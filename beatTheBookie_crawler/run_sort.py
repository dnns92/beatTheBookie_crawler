from beatTheBookie_crawler.sort_games import PastGamesFilter


if __name__ == '__main__':
    pgf = PastGamesFilter("crawler/bets/")
    pgf.run()
