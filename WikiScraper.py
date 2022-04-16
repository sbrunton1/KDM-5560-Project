import re

import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('ieer')
nltk.download('conll2002')

from bs4 import BeautifulSoup
import requests


class WikiScraper:
    """
    Scrapes text from wiki pages to be made into corpus files.
    """

    def __init__(self):
        pass

    all_text = []

    def scrape(self):
        self.page_scrape("https://eldenring.wiki.fextralife.com/Elden+Ring")
        self.get_relationships()

    def page_scrape(self, url):
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")

        content = soup.find(id="wiki-content-block").find_all("p", attrs={'class': None})
        paragraphs = []
        for doc in content:
            if len(nltk.sent_tokenize(doc.getText())) > 1:
                paragraphs.append(nltk.sent_tokenize(doc.getText()))

        for paragraph in paragraphs:
            for sentence in paragraph:
                self.all_text.append(sentence)

    def get_relationships(self):
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in self.all_text]
        tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
        chunked_sentences = [nltk.ne_chunk(sentence) for sentence in tagged_sentences]

        IS = re.compile(r'.*\bis\b(?!\b.+ing)')
        for i in range(len(chunked_sentences)):
            for rel in nltk.sem.extract_rels('PERSON', 'ORGANIZATION', chunked_sentences[i], corpus='ace', pattern=IS):
                print(self.all_text[i])

    def create_topics(self):
        print(test)