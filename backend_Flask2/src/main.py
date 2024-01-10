# Import necessary libraries and modules
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from gensim.models import Word2Vec
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from sklearn.preprocessing import MinMaxScaler

#--------------------------------------------ML Code -------------------------------------------
# Load your datasets and preprocess as needed
df1 = pd.read_csv("C:/Users/damia/Downloads/GradingSystemML-master/DataSet1.csv")
df2 = pd.read_csv("C:/Users/damia/Downloads/GradingSystemML-master/DataSet2.csv")
df = pd.merge(df1, df2, on='Question_id')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from gensim.models import Word2Vec
import pandas as pd

# Load your datasets
df1 = pd.read_csv("C:/Users/damia/Downloads/GradingSystemML-master/DataSet1.csv")
df2 = pd.read_csv("C:/Users/damia/Downloads/GradingSystemML-master/DataSet2.csv")
df = pd.merge(df1, df2, on='Question_id')

# Tokenization
df['Answers'] = df['Answers'].apply(word_tokenize)

# Drop stop words
stop_words = set(stopwords.words('Arabic'))
df['Answers'] = df['Answers'].apply(lambda x: [w for w in x if not w in stop_words])

# Lemmatization & stemming
stemmer = PorterStemmer()
df['Answers'] = df['Answers'].apply(lambda x: [stemmer.stem(word) for word in x])

lemmatizer = WordNetLemmatizer()
df['Answers'] = df['Answers'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

# Word2Vec
model = Word2Vec(df['Answers'], min_count=1)

# Vectorize responses
max_len = model.vector_size

W = np.zeros((len(df['Answers']), max_len))
for i, sentence in enumerate(df['Answers']):
    word_vectors = []
    for word in sentence:
        if word in model.wv:
            word_vectors.append(model.wv[word])
    if len(word_vectors) > 0:
        mean_vector = np.mean(word_vectors, axis=0)
        W[i, :] = mean_vector


# Define the Complex LSTM model
class ComplexLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_layers=2):
        super(ComplexLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers=num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
        self.num_layers = num_layers

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Assuming you already have 'existing_answers_vectors' and 'df' available
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
X_train, X_test, y_train, y_test = train_test_split(existing_answers_vectors, df[df['Question_id'] == question_id]['Score'], test_size=0.2, random_state=42)

# Scale input data to [0, 1] range
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32)


# Create the Complex LSTM model
complex_lstm_model = ComplexLSTM(input_size, hidden_size, output_size, num_layers)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(complex_lstm_model.parameters(), lr=0.001)

import torch
import torch.nn as nn
import torch.optim as optim

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


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Get the response text from the request
    response_text = request.json['response']

   # Import the necessary libraries
from flask import request, jsonify

# Assuming that your ComplexLSTM model is defined and loaded as complex_lstm_model

# Tokenize, preprocess, and vectorize the response
def preprocess_response(response):
    # Tokenize the response text
    response_tokens = nltk.word_tokenize(response)

    # Remove stop words from the response
    response_tokens = [w for w in response_tokens if not w in stop_words]

    # Apply stemming to the response
    response_tokens = [stemmer.stem(word) for word in response_tokens]

    # Apply lemmatization to the response
    response_tokens = [lemmatizer.lemmatize(word) for word in response_tokens]

    # Vectorize the response using the Word2Vec model
    response_vector = np.mean([model.wv[word] for word in response_tokens if word in model.wv], axis=0)

    return response_vector

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Get the response text from the request
    response_text = request.json['response']

    # Preprocess the response text and convert it to a NumPy array
    response_vector = preprocess_response(response_text)
    response_vector = torch.from_numpy(response_vector).float().unsqueeze(0)

    # Make the prediction using the Complex LSTM model
    with torch.no_grad():
        score_prediction = complex_lstm_model(response_vector.unsqueeze(1))

    predicted_score = score_prediction.item()

    # Return the predicted score as JSON
    return jsonify({'predicted_score': predicted_score})


    # Convert data to PyTorch tensor
    response_vector_tensor = torch.tensor(response_vector, dtype=torch.float32).unsqueeze(0)

    # Make prediction using the Complex LSTM model
    with torch.no_grad():
        score_prediction = complex_lstm_model(response_vector_tensor.unsqueeze(1))

    predicted_score = score_prediction.item()

    # Return the predicted score as JSON response
    return jsonify({"predicted_score": predicted_score})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
