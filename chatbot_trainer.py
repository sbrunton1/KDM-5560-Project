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


def retrain_model():
    new_bot = ChatBot()
    new_bot.initialize_training()

class ChatBot:

    lbl_encoder = LabelEncoder()
    tokenizer = Tokenizer(num_words=2000, oov_token="Unknown pattern")

    def __init__(self):
        pass

    def initialize_training(self):
        # clear keras model each training session
        keras.backend.clear_session()

        # Setup variables used for training.
        sentences = []
        responses = []
        t_labels = []
        labels = []

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

        self.lbl_encoder.fit(t_labels)
        t_labels = self.lbl_encoder.transform(t_labels)

        self.generate_model(self.fitting_variables(sentences), t_labels, topics)
        self.save_trained_data()

    def fitting_variables(self, sentences):
        self.tokenizer.fit_on_texts(sentences)
        word_index = self.tokenizer.word_index
        sequences = self.tokenizer.texts_to_sequences(sentences)
        padded_sequences = pad_sequences(sequences, truncating='post', maxlen=20)
        return padded_sequences

    def generate_model(self, padded_sequences, t_labels, topics):
        model = Sequential([
            Embedding(2000, 32, input_length=50),
            GlobalAveragePooling1D(),
            Dense(256, activation='relu'),
            Dense(256, activation='relu'),
            Dense(topics, activation='softmax')
        ])

        model.compile(loss='sparse_categorical_crossentropy',
                      optimizer='adam', metrics=['accuracy'])

        model.summary()

        model.fit(padded_sequences, np.array(t_labels), epochs=1000)

        # to save the trained model
        model.save("chat_model")

    def save_trained_data(self):
        # to save the fitted tokenizer
        with open('training_data/tokenizer.pickle', 'wb') as handle:
            pickle.dump(self.tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

        # to save the fitted label encoder
        with open('training_data/label_encoder.pickle', 'wb') as ecn_file:
            pickle.dump(self.lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    bot = ChatBot()
    bot.initialize_training()