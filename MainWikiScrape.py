import csv
import re
import stanza
import nltk
import json
import requests
import time
import os
from stanza.server import CoreNLPClient
from bs4 import BeautifulSoup
import WikiScraper
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('ieer')
nltk.download('conll2002')

URLlist = ["https://eldenring.wiki.fextralife.com/Minor+Erdtree+(Dragonbarrow)",
           "https://eldenring.wiki.fextralife.com/Impaler's+Catacombs",
           "https://eldenring.wiki.fextralife.com/Great+Horned+Tragoth",
           "https://eldenring.wiki.fextralife.com/Ancestor+Spirit",
           "https://eldenring.wiki.fextralife.com/Crystal+Bud",
           "https://eldenring.wiki.fextralife.com/Freezing+Grease",
           "https://eldenring.wiki.fextralife.com/Red-Hot+Whetblade",
           "https://eldenring.wiki.fextralife.com/Summonwater+Village",
           "https://eldenring.wiki.fextralife.com/Dog",
           "https://eldenring.wiki.fextralife.com/Runes",
           "https://eldenring.wiki.fextralife.com/Dragonkin+Soldier",
           "https://eldenring.wiki.fextralife.com/Freezing+Pot"]

scrape = WikiScraper.WikiScraper()
for x in URLlist:
    scrape.scrape(x)
