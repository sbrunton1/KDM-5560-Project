from utils import WikiScraper, trainingDataUtils
scraper = WikiScraper.WikiScraper()
scraper.scrape("https://eldenring.wiki.fextralife.com/Ashes+of+War")

trainingDataUtils = trainingDataUtils.trainingDataUtils(scraper.get_text())
trainingDataUtils.generate_tokens_from_topic(scraper.get_topic())
trainingDataUtils.append_tokens()
