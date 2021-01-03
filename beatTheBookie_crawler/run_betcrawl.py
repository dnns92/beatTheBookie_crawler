import json
from beatTheBookie_crawler.crawler.crawler import BetCrawler
from beatTheBookie_crawler.crawler.crawler import ThreeWayBetExtractor
from beatTheBookie_crawler.crawler.robotsChecker import WettPortalComRobotsChecker


if __name__ == '__main__':
    checker = WettPortalComRobotsChecker()
    bc = BetCrawler(checker, ThreeWayBetExtractor, r"crawler\matches\Sun_Jan__3_10_35_38_2021.json")
    bc.crawl()
