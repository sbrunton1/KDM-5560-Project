import json, logging, sys
import os
import re
import requests
import stanza
import time
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def append_tokens(training_data):
    logging.info(training_data)
    with open('training_data/training.json', 'r+') as file:
        file_data = json.load(file)
        for topic in training_data:
            if topic not in file_data["topics"]:
                file_data["topics"].append(topic)
        file.seek(0)
        json.dump(file_data, file, indent=4)


def compare_terms(topic, subject):
    sw = stopwords.words('english')
    topic_list = word_tokenize(topic)
    subject_list = word_tokenize(subject)
    l1 = []
    l2 = []

    topic_set = {w for w in topic_list if not w in sw}
    subject_set = {w for w in subject_list if not w in sw}

    r_vector = topic_set.union(subject_set)
    for w in r_vector:
        if w in topic_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in subject_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    for i in range(len(r_vector)):
        c += l1[i] * l2[i]

    if sum(l1) == 0 or sum(l2) == 0:
        return 0

    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)

    return cosine


def space_swap(lst):
    text_mod = []
    for s in lst:
        text_mod.append(str(s).replace(u'\xa0', u' '))
    return text_mod


class trainingDataUtils:
    """
    Utilities class for collection and modification of data to be used in training.
    """
    training_data = []
    all_text = []

    def __init__(self, text):
        self.all_text = text

    # Getters
    def get_token_sent(self):
        tokenized_sentences = [nltk.sent_tokenize(sentence) for sentence in self.all_text]
        return self.space_swap(tokenized_sentences)


    def get_all_text(self):
        return self.all_text

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
            subjects = self.get_subjects(text)
            if topic in text:
                for subject in subjects:
                    cosine = compare_terms(topic, subject)
                    if cosine > 0.5:
                        if text not in responses:
                            responses.append(text)

        self.training_data.append({
            "topic": topic,
            "inputs": [
                "What are {}".format(topic),
                "What is {}".format(topic),
                "What can you tell me about {}".format(topic),
                "What about {}".format(topic),
                topic
            ],
            "responses": responses
        })

    def get_subjects(self, text):
        nlp = spacy.load('en_core_web_sm')
        sentences = [i for i in nlp(text).sents]
        sub_tokens = []

        for sentence in sentences:
            doc = nlp(str(sentence))
            sub_tokens = [str(tok) for tok in doc if (tok.dep_ == "nsubj")]

        return sub_tokens
