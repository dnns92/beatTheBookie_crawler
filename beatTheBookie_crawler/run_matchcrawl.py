from beatTheBookie_crawler.crawler.crawler import MatchCrawler
from beatTheBookie_crawler.crawler.robotsChecker import WettPortalComRobotsChecker


if __name__ == '__main__':
    checker = WettPortalComRobotsChecker()
    cfg = "crawler/config.json"
    mc = MatchCrawler(checker, cfg, save_htmls=True)
    mc.crawl()
