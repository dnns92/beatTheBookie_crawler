from beatTheBookie_crawler.sort_games import PastGamesFilter
from beatTheBookie_crawler.dirs import BET_DIR

if __name__ == '__main__':
    pgf = PastGamesFilter(BET_DIR)
    pgf.run()
