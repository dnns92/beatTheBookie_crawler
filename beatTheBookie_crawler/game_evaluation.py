from glob import glob
import json

import numpy as np

from beatTheBookie_crawler.crawler.crawler_constants import BET_SAFETY_MARGIN


class ProbabilitiesFrom3WayOdds:
    def __init__(self, safety_margin=BET_SAFETY_MARGIN):
        self.safety_margin = safety_margin
        self.translator = FileAdapter

    def evaluate_jsons(self, glob_pattern) -> dict:
        files = glob(glob_pattern)
        profitable_bets = {}
        for file in files:
            game_odds = self.translator(file).translate()
            avg_odds, best_bookies, max_odds = self.bookie_statistics(game_odds)
            estimated_profit_home, estimated_profit_draw, estimated_profit_away = self.estimated_profits(avg_odds,
                                                                                                         max_odds)

            # which is unecessary for evaluation, but nice for logging
            best_odd, bookie, contestor = self.get_most_profitable(estimated_profit_home,
                                                                   estimated_profit_draw,
                                                                   estimated_profit_away,
                                                                   best_bookies)
            if self.is_profitable(best_odd):
                match = self.translator(file).get_current_match()
                print("-" * 10 + f"I found a profitable Bet in file {file}: {bookie}: {best_odd}-{contestor}" + "-" * 10)
                game_odds["best_odds"] = [bookie, best_odd, contestor]
                profitable_bets[match] = game_odds

        return profitable_bets

    def estimated_profits(self, avg_odds: np.ndarray, max_odds: np.ndarray):
        return (1/avg_odds - self.safety_margin) * max_odds

    @staticmethod
    def bookie_statistics(odds: dict) -> tuple:
        """
        example stucture of input odds:
        {
        "bwin": [3.00, 3.00, 2.00]  # i.e. home, draw, away
        }
        """
        max_odds = [0, 0, 0]
        best_bookies = ["", "", ""]
        sum_home_draw_away = np.zeros(3, dtype=np.float)
        ctr = 0
        # FIXME: there should be a nicer, pythonic to update this
        for bookie, odd in odds.items():
            if odd[0] > max_odds[0]:
                max_odds[0] = odd[0]
                best_bookies[0] = bookie
            if odd[1] > max_odds[1]:
                max_odds[1] = odd[1]
                best_bookies[1] = bookie
            if odd[2] > max_odds[2]:
                max_odds[2] = odd[2]
                best_bookies[2] = bookie
            sum_home_draw_away += np.array(odd)
            ctr += 1
        avg_odds = sum_home_draw_away / ctr
        return avg_odds, best_bookies, max_odds

    @staticmethod
    def is_profitable(odds: np.ndarray):
        return odds > 1.0

    @staticmethod
    def get_most_profitable(home, draw, away, bookies):
        odds = [home, draw, away]
        index = np.argmax(odds, axis=0)
        bet_type = "home" * int(odds[index] == home) + "draw" * int(odds[index] == draw) + "away" * int(odds[index] == away)
        return odds[index], bookies[index], bet_type


class FileAdapter:
    def __init__(self, file):
        """translates game json into readable format for ProbabilitiesFromOdds."""
        self.file = file

    def get_current_match(self) -> str:
        game_info = json.load(open(self.file, "r", encoding='utf-8'))
        return game_info["game"]

    def translate(self) -> dict:
        """translated to:
        {bookie1: [home, draw, away], bookie2: [home, draw, away] ...}
        """
        ret = {}
        game_info = json.load(open(self.file, "r", encoding='utf-8'))
        for bookie, odds in game_info["bookies"].items():
            if bookie in ["game", "last_pull"]: continue
            # just take the last pulled ones
            ret[bookie] = [float(odds["home"]),
                           float(odds["draw"]),
                           float(odds["away"])]
        return ret

    @staticmethod
    def get_latest_odd(dates): pass  # not needed in v1

