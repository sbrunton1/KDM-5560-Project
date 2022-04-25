import json, logging, random, pickle
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request, redirect, url_for, Markup
from chatbot_trainer import retrain_model
from utils.trainingDataUtils import append_tokens
from utils import WikiScraper, trainingDataUtils

# Create the flask app
app = Flask(__name__)
app.config["DEBUG"] = True


# Form data which will track conversation  between the user and the bot.
form_data = []

URLlist = []
# scrape = WikiScraper.WikiScraper()

# Wikiscraper stuff
# with open('training_data/urls.csv') as urlcsv:
#     csv_reader = csv.reader(urlcsv)
#     for row in csv_reader:
#         row = str(row).replace("']", "")
#         URLlist.append(str(row).replace("['", ""))
#         print(row)
#
# for x in URLlist:
#     scrape.scrape(x)
# scrape.append_tokens()

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
def chat_home():
    return render_template('form.html', form_data = form_data)

# Send user input to chatbot, pass through chatbot response function
# and append request/response to chat list.
@app.route('/', methods = ['POST'])
def send_chat():
    global previous_topic
    input = request.form.get('chat_input')

    if input == "clear":
        form_data.clear()
        return redirect(url_for('chat_home'))

    # Getting response confidence intervals
    result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([input]),
                                                                      truncating='post', maxlen=max_len))

    if result[0][np.argmax(result)] < 0.99:
        tag = "unknown"
    else:
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

    if tag == "know_more" and previous_topic is not None:
        tag = previous_topic

    previous_topic = tag

    response = ""

    for i in training_data['topics']:
        if i['topic'] == tag:
            response = Markup(np.random.choice(i['responses']))

    form_data.append((
        request.form.get('chat_input'), response
    ))

    return redirect(url_for('chat_home'))

# Additional training homepage
@app.route('/training', methods = ['GET'])
def training_home():
    return render_template('user_training.html', form_data=training_data)

@app.route('/training/manual', methods = ['POST'])
def manual_training():
    new_data = []
    questions = [question for question in request.form.get('inputs').split(',')]
    responses = [response for response in request.form.get('responses').split(',')]
    topic = request.form.get('new_topic')
    questions.extend([
            "What is {}".format(topic),
            "What can you tell me about {}".format(topic),
            "What about {}".format(topic),
            topic
        ])
    new_data.append({
        "topic": topic,
        "inputs": questions,
        "responses": responses
    })

    append_tokens(new_data)
    retrain_model()
    wait(10)
    return redirect(url_for('chat_home'))

@app.route('/training/link', methods = ['POST'])
def link_training():
    scraper = WikiScraper.WikiScraper()
    scraper.scrape(request.form.get('wiki_link'))

    tdu = trainingDataUtils.trainingDataUtils(scraper.get_text())
    tdu.generate_tokens_from_topic(scraper.get_topic())
    tdu.append_tokens()
    tdu.stop_client()
    retrain_model()

    return redirect(url_for('chat_home'))
# Instantiates app runtime.
app.run()