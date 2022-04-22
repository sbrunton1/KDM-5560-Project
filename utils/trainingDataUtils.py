import json
import os
import re
import requests
import stanza
import time
from stanza.server import CoreNLPClient


class trainingDataUtils:
    """
    Utilities class for collection and modification of data to be used in training.

    If you leave a port open run the following
    netstat -ano | findstr :9001
    taskkill /PID <enter your Pid> /f
    """
    training_data = []
    all_text = []
    client = None

    def __init__(self, text):
        self.all_text = text

        # Download the Stanford CoreNLP package with Stanza's installation command
        # This'll take several minutes, depending on the network speed
        corenlp_dir = '../corenlp'
        stanza.install_corenlp(dir=corenlp_dir)

        # Set the CORENLP_HOME environment variable to point to the installation location
        os.environ["CORENLP_HOME"] = corenlp_dir
        self.client = CoreNLPClient(timeout=15000, be_quiet=True, annotators=['openie'],
                                    endpoint='http://localhost:9001')
        self.client.start()
        time.sleep(10)

    # Getters
    def get_token_sent(self):
        tokenized_sentences = [nltk.sent_tokenize(sentence) for sentence in self.all_text]
        return self.space_swap(tokenized_sentences)


    def get_all_text(self):
        return self.all_text

    def generate_training_tokens(self):
        postags = ['NNPS', 'NNP', 'NNS']
        topic = ""
        responses = []
        for text in self.all_text:
            document = self.client.annotate(text, annotators='pos', output_format='json')
            for sentence in document['sentences']:
                for token in sentence['tokens']:
                    if (token['pos'] in postags) or (token['index'] == 1 and 'NN' in token['pos']):
                        topic = token['word']

                if topic in text:
                    responses.append(text)

            self.training_data.append({
                "topic": topic,
                "inputs": [
                    "What is {}".format(topic),
                    "What can you tell me about {}".format(topic),
                    "What about {}".format(topic),
                    topic
                ],
                "responses": responses
            })


    def append_tokens(self):
        with open('training_data/training.json', 'r+') as file:
            file_data = json.load(file)
            for topic in self.training_data:
                if topic not in file_data["topics"]:
                    file_data["topics"].append(topic)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def generate_tokens_from_topic(self, topic):
        responses = []

        for text in self.all_text:
            triplets = self.get_triplets(text)
            if topic in text:
                for i in triplets:
                    if topic == i['subject']:
                        if text not in responses:
                            responses.append(text)

        self.training_data.append({
            "topic": topic,
            "inputs": [
                "What is {}".format(topic),
                "What can you tell me about {}".format(topic),
                "What about {}".format(topic),
                topic
            ],
            "responses": responses
        })

    def get_triplets(self, text):
        triples = []
        document = self.client.annotate(text, annotators='openie', output_format='json')
        for sentence in document['sentences']:
            for triple in sentence['openie']:
                triples.append({
                    'subject': triple['subject'],
                    'relation': triple['relation'],
                    'object': triple['object']
                })
        return triples

    # Utility methods
    def space_swap(self, lst):
        text_mod = []
        for s in lst:
            text_mod.append(str(s).replace(u'\xa0', u' '))
        return text_mod


    def stop_client(self):
        self.client.stop()