from beatTheBookie_crawler.crawler.crawler import BetCrawler
from beatTheBookie_crawler.crawler.crawler import ThreeWayBetExtractor
from beatTheBookie_crawler.crawler.robotsChecker import WettPortalComRobotsChecker
from beatTheBookie_crawler.game_evaluation import ProbabilitiesFrom3WayOdds
from beatTheBookie_crawler.crawler.crawler import Crawler
from beatTheBookie_crawler.crawler.crawler import MatchCrawler
from beatTheBookie_crawler.crawler.crawler import ResultCrawler
from beatTheBookie_crawler.sort_games import PastGamesFilter


if __name__ == '__main__':
    checker = WettPortalComRobotsChecker()

    cfg = "crawler/config.json"
    mc = MatchCrawler(checker, cfg, save_htmls=True, return_filename=True)
    fn = mc.crawl()

    bc = BetCrawler(checker, ThreeWayBetExtractor, fn)
    bc.crawl()

    pgf = PastGamesFilter("crawler/bets/")
    pgf.run()

    uge = ProbabilitiesFrom3WayOdds()
    uge.evaluate_jsons("crawler/bets/*.json")
    uge.dump(Crawler.create_timestring()[0])

    rc = ResultCrawler(checker, "crawler/profitables", "crawler/paperbets/")
    rc.crawl()
