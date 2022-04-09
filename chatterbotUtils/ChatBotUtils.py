from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import logging


"""
# Function for initial training of model.
# As of right now, this function simply trains the model on a single conversation block.
# this limits the model to very rudimentary responses based on the words that it knows.
"""

def basicTraining(bot):
    logging.basicConfig(level=logging.INFO)

    trainer = ChatterBotCorpusTrainer(bot)

    trainer.train(
        'chatterbot.corpus.english'
    )

"""
# Function which takes a trained bot model and user input 
# and returns the response derived from training.
"""

def response(request, bot):
    bot_response = bot.get_response(request)

    return bot_response
