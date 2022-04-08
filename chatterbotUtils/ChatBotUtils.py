from chatterbot.trainers import ListTrainer

"""
# Function for initial training of model.
# As of right now, this function simply trains the model on a single conversation block.
# this limits the model to very rudimentary responses based on the words that it knows.
"""

def basicTraining(bot):
    small_talk = ['hi there!',
                  'hi!',
                  'how do you do?',
                  'how are you?',
                  'i\'m cool.',
                  'fine, you?',
                  'always cool.',
                  'i\'m ok',
                  'glad to hear that.',
                  'i\'m fine',
                  'glad to hear that.',
                  'i feel awesome',
                  'excellent, glad to hear that.',
                  'not so good',
                  'sorry to hear that.',
                  'what\'s your name?',
                  'i\'m pybot. ask me a math question, please.']

    list_trainer = ListTrainer(bot)

    for item in small_talk:
        list_trainer.train(item)


"""
# Function which takes a trained bot model and user input 
# and returns the response derived from training.
"""

def response(request, bot):
    print(request)
    bot_response = bot.get_response(request)
    print(bot_response)

    return bot_response
