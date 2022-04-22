import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

#set of links within the Elden Ring Wiki
internal_urls = set()

#ensures validity of url
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

#Return list of URLs found on "url"
def get_links(url):
    urls = set()
    domain_name = urlparse(url).netloc #pulls domain name to verify internal link
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        #clean up relative links
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

def crawl(url, max_urls = 30):
    global urls_visited
    urls_visited += 1
    links = get_links(url)
    for link in links:
        if urls_visited > max_urls:
            break
        crawl(link, max_urls = max_urls)

if __name__ == "__main__":
    crawl("https://eldenring.wiki.fextralife.com/Elden+Ring+Wiki")
    print("[+] Total Internal links:", len(internal_urls))

print(internal_urls)