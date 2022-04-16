import json
import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

# clear keras model each training session
keras.backend.clear_session()

# Setup variables used for training.
sentences = []
responses = []
t_labels = []
labels = []
lbl_encoder = LabelEncoder()
tokenizer = Tokenizer(num_words=2000, oov_token="Unknown pattern")

with open('training_data/training.json') as file:
    data = json.load(file)

for intent in data['topics']:
    if intent['topic'] not in labels:
        labels.append(intent['topic'])

    for pattern in intent['inputs']:
        sentences.append(pattern)
        t_labels.append(intent['topic'])
    responses.append(intent['responses'])

topics = len(labels)

lbl_encoder.fit(t_labels)
t_labels = lbl_encoder.transform(t_labels)

tokenizer.fit_on_texts(sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=20)

model = Sequential([
    Embedding(2000, 16, input_length=20),
    GlobalAveragePooling1D(),
    Dense(16, activation='relu'),
    Dense(16, activation='relu'),
    Dense(topics, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])

model.summary()

history = model.fit(padded_sequences, np.array(t_labels), epochs=1000)

# to save the trained model
model.save("chat_model")

# to save the fitted tokenizer
with open('training_data/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# to save the fitted label encoder
with open('training_data/label_encoder.pickle', 'wb') as ecn_file:
    pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)