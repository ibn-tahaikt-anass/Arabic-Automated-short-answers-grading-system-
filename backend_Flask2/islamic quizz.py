#!/usr/bin/env python
# coding: utf-8

# In[20]:


import numpy as np
import pandas as pd
import warnings 
warnings.filterwarnings('ignore')


# In[21]:


#load data
df1 = pd.read_csv(r'C:/Users/damia/OneDrive/Bureau/Backend/dataset1.csv')
df2 = pd.read_csv(r'C:/Users/damia/OneDrive/Bureau/Backend/dataset2.csv')


# In[22]:


df1.head()


# In[ ]:





# In[23]:


#merge the datasets 
df= pd.merge(df1,df2,on='Question_id')
df.head()


# In[24]:


#returning a statistical summary about the dataset
df.describe(include="all")


# In[25]:


#prétraitement des données en utilisant NLTK de NLP
import nltk


# In[26]:


# Tokenisation, déviser le texte en une séquence de tokens
from nltk.tokenize import word_tokenize
# Replace NaN values with an empty string
df['answers']=df['answers'].fillna('')
# Convert lists to strings
df['answers'] = df['answers'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)
# Apply tokenization
df['answers'] = df['answers'].apply(word_tokenize)


# In[27]:


df['answers'].head()


# In[28]:


#Drop stop words
from nltk.corpus import stopwords

stop_words = set(stopwords.words('Arabic'))
stop_words


# In[29]:


df['answers'] = df['answers'].apply(lambda x: [w for w in x if not w in stop_words])


# In[30]:


#Lemmatization & stemming
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
# Stem words in answers column
df['answers'] = df['answers'].apply(lambda x: [stemmer.stem(word) for word in x])

lemmatizer = WordNetLemmatizer()
# Lemmatize words in answers column
df['answers'] = df['answers'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

df.head()


# In[31]:


#encodage des mots 
#création de modèle
#Word2Vec
from gensim.models import Word2Vec
model = Word2Vec(df['answers'], min_count=1)


# In[32]:


#véctoriser les réponses 
max_len = model.vector_size

W = np.zeros((len(df['answers']), max_len))
for i, sentence in enumerate(df['answers']):
    word_vectors = []
    for word in sentence:
        if word in model.wv:
            word_vectors.append(model.wv[word])
    if len(word_vectors) > 0:
        mean_vector = np.mean(word_vectors, axis=0)
        W[i, :] = mean_vector


# In[33]:


#vocabulaire des mots
vocab_list = model.wv.index_to_key

#get a dictionary mapping each word to its index in the word vectors 
vocab_dict = model.wv.key_to_index
print(vocab_dict)


# In[34]:


#tester le modèle word2vec 1
word=model.wv['الكوثر']
print(word)


# In[35]:


#tester le modèle word2vec 2
#calculer la similarité entre 2 mots 
word1="البقرة"
word2="البقرة"

similarity = model.wv.similarity(word1,word2)
print(f"Similarity between {word1} and {word2} is: {similarity}")


# In[36]:


# Demander à l'utilisateur d'entrer une réponse et un id de question
question_id= 1
response = "أطول سورة في القرآن الكريم هي سورة البقرة"


# In[37]:


# Tokeniser la réponse entrée
response_tokens = nltk.word_tokenize(response)

# Supprimer les mots d'arrêt de la réponse
response_tokens = [w for w in response_tokens if not w in stop_words]

# Appliquer le stemming à la réponse
response_tokens = [stemmer.stem(word) for word in response_tokens]

# Appliquer la lemmatisation à la réponse
response_tokens = [lemmatizer.lemmatize(word) for word in response_tokens]

# Vectoriser la réponse en utilisant le modèle Word2Vec
response_vector = np.mean([model.wv[word] for word in response_tokens if word in model.wv], axis=0)

response_vector
response_tokens


# In[ ]:





# In[ ]:





# In[ ]:





# In[48]:


import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def find_existing_answers_vectors(df, question_id, W):

    if question_id in df['Question_id'].values:
        # Trouver tous les indices correspondants à l'ID de la question
        question_indices = df.index[df['Question_id'] == question_id].tolist()

        # Extraire les vecteurs de réponse correspondants à partir de la matrice W
        existing_answers_vectors = []
        for i in question_indices:
            existing_answers_vectors.append(W[i])
    else:
        print("L'ID de la question que vous avez fourni est incorrect")
        existing_answers_vectors = None
    existing_answers_vectors = np.array(existing_answers_vectors)
    return existing_answers_vectors
    pass

existing_answers_vectors = find_existing_answers_vectors(df, question_id, W)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(existing_answers_vectors, df[df['Question_id'] == question_id]['score'], test_size=0.2, random_state=42)

# Scale input data to [0, 1] range
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32)

# Define the Complex RNN model
class ComplexRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=2):
        super(ComplexRNN, self).__init__()
        self.rnn = nn.RNN(input_size, hidden_size, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.num_layers = num_layers
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), hidden_size).to(x.device)  # Initialize hidden state
        out, _ = self.rnn(x, h0)
        out = self.fc(out[:, -1, :])  # Using the last time step's output
        return out

input_size = X_train_tensor.shape[1]
hidden_size = 30  # Increased hidden size
output_size = 1  # Assuming a single output for regression
num_layers = 5  # Increased number of layers

# Create the Complex RNN model
complex_rnn_model = ComplexRNN(input_size, hidden_size, output_size, num_layers)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(complex_rnn_model.parameters(), lr=0.001)

# Training the Complex RNN model
num_epochs = 200
batch_size = 5

for epoch in range(num_epochs):
    permutation = torch.randperm(X_train_tensor.size(0))
    for i in range(0, X_train_tensor.size(0), batch_size):
        indices = permutation[i:i + batch_size]
        batch_x, batch_y = X_train_tensor[indices], y_train_tensor[indices]
        
        optimizer.zero_grad()
        outputs = complex_rnn_model(batch_x.unsqueeze(1))
        loss = criterion(outputs.squeeze(), batch_y)
        loss.backward()
        optimizer.step()
    
    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Calculate RMSE on test set
with torch.no_grad():
    test_outputs = complex_rnn_model(X_test_tensor.unsqueeze(1))
    test_loss = criterion(test_outputs.squeeze(), y_test_tensor)
    rmse = torch.sqrt(test_loss).item()
    print(f'RMSE on test set: {rmse:.4f}')

# Prediction for a new response vector (assuming 'response_vector' is defined)
new_response_vector = torch.from_numpy(response_vector).float().unsqueeze(0)

with torch.no_grad():
    score_prediction = complex_rnn_model(new_response_vector.unsqueeze(0))

predicted_score = score_prediction.item()

# Real score from your dataset column 'score'
real_scores = df[df['Question_id'] == question_id]['score'].values
if len(real_scores) > 0:
    real_score = real_scores[0]  # Assuming only one real score per question_id
    print(f"Question_id: {question_id}, RealScore: {real_score}, PredictedScore: {predicted_score}")
else:
    print(f"No real score found for Question_id: {question_id}")


# In[46]:


import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Suppose you have defined functions and data structures like 'find_existing_answers_vectors', 'df', 'question_id', 'W', and 'response_vector' previously

# Function to find existing answers vectors (assuming it's defined somewhere)
def find_existing_answers_vectors(df, question_id, W):

    if question_id in df['Question_id'].values:
        # Trouver tous les indices correspondants à l'ID de la question
        question_indices = df.index[df['Question_id'] == question_id].tolist()

        # Extraire les vecteurs de réponse correspondants à partir de la matrice W
        existing_answers_vectors = []
        for i in question_indices:
            existing_answers_vectors.append(W[i])
    else:
        print("L'ID de la question que vous avez fourni est incorrect")
        existing_answers_vectors = None
    existing_answers_vectors = np.array(existing_answers_vectors)
    return existing_answers_vectors
    pass

# Define the Complex LSTM model
class ComplexLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=2):
        super(ComplexLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.num_layers = num_layers
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), hidden_size).to(x.device)  # Initialize hidden state
        c0 = torch.zeros(self.num_layers, x.size(0), hidden_size).to(x.device)  # Initialize cell state
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])  # Using the last time step's output
        return out

# Assuming X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor are already defined

input_size = X_train_tensor.shape[1]
hidden_size = 30  # Increased hidden size
output_size = 1  # Assuming a single output for regression
num_layers = 10 # Increased number of layers

# Create the Complex LSTM model
complex_lstm_model = ComplexLSTM(input_size, hidden_size, output_size, num_layers)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(complex_lstm_model.parameters(), lr=0.001)

# Training the Complex LSTM model
num_epochs = 200
batch_size = 5

for epoch in range(num_epochs):
    permutation = torch.randperm(X_train_tensor.size(0))
    for i in range(0, X_train_tensor.size(0), batch_size):
        indices = permutation[i:i + batch_size]
        batch_x, batch_y = X_train_tensor[indices], y_train_tensor[indices]
        
        optimizer.zero_grad()
        outputs = complex_lstm_model(batch_x.unsqueeze(1))
        loss = criterion(outputs.squeeze(), batch_y)
        loss.backward()
        optimizer.step()
    
    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Prediction for a new response vector (assuming 'response_vector' is defined)
new_response_vector = torch.from_numpy(response_vector).float().unsqueeze(0)

with torch.no_grad():
    score_prediction = complex_lstm_model(new_response_vector.unsqueeze(0))

predicted_score = score_prediction.item()

# Real score from your dataset column 'score'
real_scores = df[df['Question_id'] == question_id]['score'].values
if len(real_scores) > 0:
    real_score = real_scores[0]  # Assuming only one real score per question_id
    print(f"Question_id: {question_id}, RealScore: {real_score}, PredictedScore: {predicted_score}")
else:
    print(f"No real score found for Question_id: {question_id}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[76]:





# In[77]:





# In[78]:





# In[79]:





# In[ ]:





# In[ ]:




