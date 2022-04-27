import json, logging, random, pickle, sys, time
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request, redirect, url_for, Markup
from chatbot_trainer import retrain_model
from utils.trainingDataUtils import append_tokens
from utils import WikiScraper, trainingDataUtils


def update_labels():
    with open("training_data/training.json") as file:
        training_data = json.load(file)

    with open('training_data/tokenizer.pickle', 'rb') as token_pic:
        tokenizer = pickle.load(token_pic)

    with open('training_data/label_encoder.pickle', 'rb') as encoded_label_pic:
        lbl_encoder = pickle.load(encoded_label_pic)

    return training_data, tokenizer, lbl_encoder

# Create the flask app
app = Flask(__name__)

# Form data which will track conversation  between the user and the bot.
form_data = []

# topic tracking
previous_topic = None

model = keras.models.load_model('chat_model')

training_data, tokenizer, lbl_encoder = update_labels()

max_len = 20


# Flask API routes for application, get method returns view of app frontend.
@app.route('/', methods=['GET'])
def chat_home():
    return render_template('form.html', form_data =form_data)

# Send user input to chatbot, pass through chatbot response function
# and append request/response to chat list.
@app.route('/', methods = ['POST'])
def send_chat():
    global previous_topic, model

    input = request.form.get('chat_input')

    if input == "clear":
        form_data.clear()
        return redirect(url_for('chat_home'))

    # Getting response confidence intervals
    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([input]),
                                                                      truncating='post', maxlen=max_len))
    accuracy = np.round(result[0][np.argmax(result)], 3)

    guess_topic = lbl_encoder.inverse_transform([np.argmax(result)])

    if accuracy < 0.90:
        topic = "unknown"
    else:
        topic = guess_topic

    if topic == "know_more" and previous_topic is not None:
        topic = previous_topic

    all_scores = [[lbl_encoder.inverse_transform(list(range(0, len(result[0])-1)))[i], np.round(result[0], 3)[i]] for i in range(len(result[0])-1)]

    print("\nThe model returned the topic: {}".format(guess_topic) +
          "\nWith an accuracy score of: {},".format(accuracy) +
          "\nScores are as follows: {}\n".format(all_scores),
        file=sys.stderr
    )
    previous_topic = topic

    response = ""

    for i in training_data['topics']:
        if i['topic'] == topic:
            response = Markup(np.random.choice(i['responses']))

    form_data.append((
        request.form.get('chat_input'), response, accuracy
    ))

    return redirect(url_for('chat_home'))

# Additional training homepage
@app.route('/training', methods = ['GET'])
def training_home():
    return render_template('user_training.html')

@app.route('/training/manual', methods = ['POST'])
def manual_training():
    global model, training_data, tokenizer, lbl_encoder

    new_data = []
    topic = request.form.get('new_topic')
    inputs = [input for input in request.form.get('inputs').split(',')] + [topic]
    responses = [response for response in request.form.get('responses').split(',')]

    new_data.append({
        "topic": topic,
        "inputs":inputs,
        "responses": responses
    })

    append_tokens(new_data)
    retrain_model()

    model = keras.models.load_model('chat_model')
    training_data, tokenizer, lbl_encoder = update_labels()

    return redirect(url_for('chat_home'))

@app.route('/training/link', methods = ['POST'])
def link_training():
    global model, training_data, tokenizer, lbl_encoder

    scraper = WikiScraper.WikiScraper()
    scraper.scrape(request.form.get('wiki_link'))

    tdu = trainingDataUtils.trainingDataUtils(scraper.get_text())
    tdu.generate_tokens_from_topic(scraper.get_topic())
    tdu.append_tokens()

    retrain_model()
    training_data, tokenizer, lbl_encoder = update_labels()

    model = keras.models.load_model('chat_model')


    return redirect(url_for('chat_home'))


if __name__ == "__main__":
    # Instantiates app runtime.
    app.run()