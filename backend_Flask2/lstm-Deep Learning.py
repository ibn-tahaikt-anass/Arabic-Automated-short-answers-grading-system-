#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import numpy as np
from keras import utils
from tensorflow.keras.callbacks import TensorBoard
from time import time
import tensorflow as tf


# In[2]:


get_ipython().system(' pip3 install gensim')


# In[3]:


from gensim.models import KeyedVectors
fasttext_model = KeyedVectors.load_word2vec_format("C:/Users/pc/Desktop/Deep Learning/wiki.ar.vec")


# In[4]:


stu_answers= pd.read_csv('C:/Users/pc/Desktop/Deep Learning/dataset2.csv', encoding='utf-8')
stu_answers = stu_answers.dropna()
stu_answers


# In[5]:


stu_answers['answers'].isnull().sum()


# In[6]:


get_ipython().system('pip install -U nltk')


# In[7]:


# preprocessing 
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import nltk
nltk.download('stopwords')
nltk.download('punkt')
# stop words
arb_stopwords = set(nltk.corpus.stopwords.words("arabic"))
nltk.download('wordnet')


from nltk.stem.arlstem import ARLSTem
stemmmer = ARLSTem()

def remove_stowords(elements):
    corps = []
    for string in elements :
        #string = string.strip()
        #string = string.split()
        string = nltk.sent_tokenize(string.strip())
        string = [ stemmmer.stem(word) for word in string if not word in arb_stopwords ]
        string = ''.join(string)
        corps.append(string)
    return corps


# In[8]:


answers = stu_answers['answers']
scores = stu_answers['score']
scores = tf.keras.utils.to_categorical(
    scores, num_classes=6, dtype='float32'
)


# In[9]:


corps = remove_stowords(answers)
scores.shape,len(corps)


# In[10]:


fasttext_model.most_similar('الملائكة')


# In[11]:


# tokenization
from keras.preprocessing.text import Tokenizer,text_to_word_sequence , one_hot , text_to_word_sequence
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


#train tokenization
tokenizer = Tokenizer(filters=''''!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ''''' )
#tokenizer = Tokenizer(filters='#' )
tokenizer.fit_on_texts(corps)
sequences = tokenizer.texts_to_sequences(corps)
#max_sequence_length = 5
max_sequence_length = max(len(s) for s in sequences)
sequences = pad_sequences(sequences,max_sequence_length)
word2idx = tokenizer.word_index
vocab_size = len(word2idx) + 1


# word embedding
from keras.layers import Embedding
import numpy as np
EMBEDDING_DIM = 300
num_words = len(word2idx) + 1
count = 0 
# prepare embedding matrix
embedding_matrix = np.zeros((num_words, EMBEDDING_DIM))
for word, idx in word2idx.items():
    if (word in fasttext_model) :
        embedding_matrix[idx] = fasttext_model.get_vector(word)
    else :
        count=count+1
        print("  word not exist in voca ---> " + word)   
    #embedding_matrix[idx] = fasttext_model.get_vector("unk")


# In[12]:


from sklearn.model_selection import train_test_split
# concatenate question number with 
X_train, X_test, y_train, y_test = train_test_split(sequences, scores, test_size=0.2)


# In[145]:


# train model
from keras.regularizers import l1
from keras.models import Sequential
from keras.layers import Dense, Embedding,Input,Dropout,Flatten
from keras.layers import LSTM
from keras.models import Model

print('Build model...')

inp = Input(shape=(max_sequence_length,))
model = Embedding(num_words,
                            EMBEDDING_DIM,
                            weights=[embedding_matrix],
                            input_length=max_sequence_length,
                            trainable=False)(inp)
model = LSTM(units=64, return_sequences=True, return_state=False ,  activation= tf.keras.activations.relu)(model)
model = Dropout(0.2)(model)
model = Flatten()(model)
model = Dense(50, activation=tf.keras.activations.relu)(model)
model = Dropout(0.2)(model)
model = Dense(6, activation=tf.keras.activations.softmax)(model)
model = Model(inputs=inp, outputs=model)


# In[146]:


from keras import backend as K

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))


# In[147]:


import tensorflow_addons as tfa
#https://neptune.ai/blog/tensorboard-tutorial
tensorboard_callback = TensorBoard(log_dir="./logs")
#Early stopping
es_callback = tf.keras.callbacks.EarlyStopping(monitor='loss',patience=3,verbose=1,mode='min')
keras_callbacks = [
  tensorboard_callback ,es_callback
]
#metrics=['accuracy',tf.keras.metrics.Precision(), tf.keras.metrics.Recall(),f1_m,tfa.metrics.CohenKappa(num_classes=3)]
# try using different optimizers and different optimizer configs
model.compile(loss='categorical_crossentropy',
              optimizer=tf.keras.optimizers.Adam(learning_rate=0.01, beta_1=0.9, beta_2=0.999),
              metrics=['accuracy',tf.keras.metrics.Precision(), tf.keras.metrics.Recall(),f1_m,tfa.metrics.CohenKappa(num_classes=6)])

model.summary()


# In[148]:


get_ipython().run_line_magic('reload_ext', 'tensorboard')
log_folder = 'logs'

print('Train...')
time_start = time()
hisotry = model.fit(X_train, y_train,batch_size=256,epochs=150,callbacks=keras_callbacks,validation_data=(X_test, y_test)) 
time_start = time() - time_start

print("Took : "+str(np.round(time_start, 2))+" (s)") 

#model.save('asag_lstm_model.h5')


# In[149]:


scores_trainig = model.evaluate(X_train, y_train, verbose=1)
print("Training Loss: %f%%" % (scores_trainig[0]))
print("Training Accuracy: %.2f%%" % (scores_trainig[1]*100))
print("Training Precision: %.2f%%" % (scores_trainig[2]*100))
print("Training Recall: %.2f%%" % (scores_trainig[3]*100))
print("Training F1 Score: %.2f%%" % (scores_trainig[4]*100))
print("Training Cohen Kappa: %.2f%%" % (scores_trainig[5]*100))


# In[150]:


scores_test = model.evaluate(X_test, y_test, verbose=1)
print("Test Loss: %f%%" % (scores_test[0]))
print("Test Accuracy: %.2f%%" % (scores_test[1]*100))
print("Test Precision: %.2f%%" % (scores_test[2]*100))
print("Test Recall: %.2f%%" % (scores_test[3]*100))
print("Test F1 Score: %.2f%%" % (scores_test[4]*100))
print("Test Cohen Kappa: %.2f%%" % (scores_test[5]*100))


# In[151]:


'''
%reload_ext tensorboard
log_folder = 'logs'
%tensorboard --logdir={log_folder}
'''
import matplotlib.pyplot as plt
print(hisotry.history.keys())

# summarize history for accuracy
plt.plot(hisotry.history['accuracy'])
plt.plot(hisotry.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(hisotry.history['loss'])
plt.plot(hisotry.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for kappa
plt.plot(hisotry.history['cohen_kappa'])
plt.plot(hisotry.history['val_cohen_kappa'])
plt.title('model loss')
plt.ylabel('cohen_kappa')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for kappa
plt.plot(hisotry.history['f1_m'])
plt.plot(hisotry.history['val_f1_m'])
plt.title('model F1')
plt.ylabel('cohen_kappa')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


# In[156]:


def predict_manual_input(model, answer, question_id):
    # Preprocess the manually input answer
    preprocessed_answer = remove_stowords([answer])

    # Tokenize and pad the sequence
    input_sequence = tokenizer.texts_to_sequences(preprocessed_answer)
    input_sequence = pad_sequences(input_sequence, maxlen=max_sequence_length)

    # Predict the score
    predicted_score = model.predict(input_sequence)[0]
    predicted_class = np.argmax(predicted_score)

    # Display the result
    print(f"Question ID: {question_id}")
    print(f"Manually Input Answer: {answer}")
    print(f"Predicted Score: {predicted_score}")
    print(f"Predicted Class: {predicted_class}")


# In[166]:


# Manually input answer and question ID
manual_answer = "البقرة هي سورة القرآن الثانية وأطولها"
manual_question_id = 1  # Replace with the desired question ID

# Predict score
predict_manual_input(model, manual_answer, manual_question_id)


# In[ ]:




