import nltk
import requests
from bs4 import BeautifulSoup

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('ieer')
nltk.download('conll2002')


class WikiScraper:
    """
    Scrapes text from wiki pages to be made into corpus files.
    """

    all_text = []
    topic = ""

    def __init__(self):
        pass

    def scrape(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        content = soup.find(id="wiki-content-block").find_all("p", attrs={'class': None})

        self.topic = soup.find("a", attrs={"id": "page-title"}).getText().split(" | ", 1)[0]

        paragraphs = []
        for doc in content:
            if len(nltk.sent_tokenize(doc.getText())) > 1:
                paragraphs.append(nltk.sent_tokenize(doc.getText()))

        for paragraph in paragraphs:
            for sentence in paragraph:
                self.all_text.append(sentence)

    def get_text(self):
        return self.all_text

    def get_topic(self):
        return self.topic

