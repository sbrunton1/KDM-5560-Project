import json, logging, random, pickle
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request, redirect, url_for

# Create the flask app
app = Flask(__name__)
app.config["DEBUG"] = True

# Form data which will track conversation  between the user and the bot.
form_data = []

# topic tracking
previous_topic = None

with open("training_data/training.json") as file:
    training_data = json.load(file)

model = keras.models.load_model('chat_model')

with open('training_data/tokenizer.pickle', 'rb') as token_pic:
    tokenizer = pickle.load(token_pic)

with open('training_data/label_encoder.pickle', 'rb') as encoded_label_pic:
    lbl_encoder = pickle.load(encoded_label_pic)

max_len = 20

# Flask API routes for application, get method returns view of app frontend.
@app.route('/', methods=['GET'])
def home():
    return render_template('form.html', form_data = form_data)

# Get form data, pass through chatbot response function and append.
@app.route('/', methods = ['POST'])
def data():
    global previous_topic
    input = request.form.get('chat_input')

    # Getting response confidence intervals
    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([input]),
                                                                      truncating='post', maxlen=max_len))

    if result[0][np.argmax(result)] < 0.98:
        tag = "unknown"
    else:
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

    if tag == "know_more" and previous_topic is not None:
        tag = previous_topic

    previous_topic = tag

    response = ""

    for i in training_data['topics']:
        if i['topic'] == tag:
            response = np.random.choice(i['responses'])

    form_data.append((
        request.form.get('chat_input'), response
    ))

    return redirect(url_for('home'))

# Instantiates app runtime.
app.run()