import json
from beatTheBookie_crawler.game_evaluation import ProbabilitiesFrom3WayOdds
from beatTheBookie_crawler.crawler.crawler import Crawler


if __name__ == '__main__':
    uge = ProbabilitiesFrom3WayOdds()
    profitable_bet_candidates = uge.evaluate_jsons("crawler/bets/*.json")

    time_, _ = Crawler.create_timestring()
    json.dump(profitable_bet_candidates,
              open(f"beatTheBookie_crawler/crawler/profitables/{time_}.json", "w", encoding="utf-8"),
              indent=4,
              sort_keys=True
              )
