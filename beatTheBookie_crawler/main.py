from beatTheBookie_crawler.crawler.crawler import BetCrawler
from beatTheBookie_crawler.crawler.crawler import ThreeWayBetExtractor
from beatTheBookie_crawler.crawler.robotsChecker import WettPortalComRobotsChecker
from beatTheBookie_crawler.game_evaluation import ProbabilitiesFrom3WayOdds
from beatTheBookie_crawler.crawler.crawler import Crawler
from beatTheBookie_crawler.crawler.crawler import MatchCrawler
from beatTheBookie_crawler.crawler.crawler import ResultCrawler
from beatTheBookie_crawler.sort_games import PastGamesFilter

from beatTheBookie_crawler.dirs import BET_DIR, PROFITABLE_DIR, PAPERBET_DIR, CRAWLER_DIR

if __name__ == '__main__':
    checker = WettPortalComRobotsChecker()

    cfg = f"{CRAWLER_DIR}/config.json"
    mc = MatchCrawler(checker, cfg, save_htmls=True, return_filename=True)
    fn = mc.crawl()

    bc = BetCrawler(checker, ThreeWayBetExtractor, fn)
    bc.crawl()

    pgf = PastGamesFilter(BET_DIR)
    pgf.run()

    uge = ProbabilitiesFrom3WayOdds()
    uge.evaluate_jsons(f"{BET_DIR}/*.json")
    uge.dump(Crawler.create_timestring()[0])

    rc = ResultCrawler(checker, PROFITABLE_DIR, PAPERBET_DIR)
    rc.crawl()
