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

    # ensures validity of url
    def is_valid(url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    # Return list of URLs found on "url"
    def get_links(url):
        urls = set()
        domain_name = urlparse(url).netloc  # pulls domain name to verify internal link
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            # clean up relative links
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not is_valid(href):
                continue
            if href in internal_urls:
                continue
            if domain_name not in href:
                continue
            urls.add(href)
            internal_urls.add(href)
        return urls

    urls_visited = 0

    def crawl(url, max_urls=30):
        global urls_visited
        urls_visited += 1
        links = get_links(url)
        for link in links:
            if urls_visited > max_urls:
                break
            crawl(link, max_urls=max_urls)

