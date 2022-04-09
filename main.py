from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbotUtils import ChatBotUtils

# Create the flask app
app = Flask(__name__)
app.config["DEBUG"] = True

# Form data which will track conversation  between the user and the bot.
form_data = []

# create instance of chat bot, train the bot using simple training function
my_bot = ChatBot(name='FlaskChatBot', read_only=True,
                     logic_adapters=['chatterbot.logic.MathematicalEvaluation',
                                     'chatterbot.logic.BestMatch'])
ChatBotUtils.basicTraining(my_bot)

# Flask API routes for application, get method returns view of app frontend.
@app.route('/', methods=['GET'])
def home():
    return render_template('form.html', form_data = form_data)

# Get form data, pass through chatbot response function and append.
@app.route('/', methods = ['POST'])
def data():
    form_data.append((
        request.form.get('chat_input'), ChatBotUtils.response(request.form.get('chat_input'), my_bot)
    ))

    return redirect(url_for('home'))

# Instantiates app runtime.
app.run()