import sys
sys.path.append("C:/Users/Lyle/PycharmProjects/ChatterBot")
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import WikiScraper
import logging

"""
Testing scraper functionality
"""
def test_scraper():
    logging.basicConfig(level=logging.INFO)

    scraper = WikiScraper.WikiScraper()

    scraper.scrape()
