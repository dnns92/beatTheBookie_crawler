import numpy as np

FRIENDLY_TIMER = 0.25  # seconds between requests
VERY_FRIENDLY_TIMER = 10
RARE_TIMER = 100000
BOOKIE_ODD_POSITIONS = [0, 2, 3, 4, 5, 6]
HISTORY_DIR = "history"
CANDIDATE_DIR = "candidates"
OFFSET_HOME_WIN, OFFSET_DRAW, OFFSET_AWAY_WIN = 0.034, 0.057, 0.037  # check paper for values
BET_SAFETY_MARGIN = np.array([OFFSET_HOME_WIN, OFFSET_DRAW, OFFSET_AWAY_WIN])
ROBOTSTXT = "https://www.wettportal.com/robots.txt"


class Result:
    home = 0
    draw = 1
    away = 2

    @staticmethod
    def eval_score(home, away):
        if home > away:
            return 0
        if home == away:
            return 1
        if away > home:
            return 2
