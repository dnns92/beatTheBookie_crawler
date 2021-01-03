import json
import time
import requests
from datetime import datetime

import regex as re
from bs4 import BeautifulSoup

from beatTheBookie_crawler.utils.robots import RobotsTxtError
from .crawler_constants import FRIENDLY_TIMER
from beatTheBookie_crawler.utils.misc import create_timestring

class Crawler:
    def __init__(self, robots_checker=None):
        """Base Class for MatchCrawler and BetCrawler
        TODO: implement more functionality here and less in the specific crawlers"""
        self.robots_checker = robots_checker

    def check_allowed(self, league_link):
        allowed = self.robots_checker.can_fetch(league_link)
        if not allowed:
            raise RobotsTxtError(league_link)

    @staticmethod
    def create_timestring():
        time_ = datetime.now()
        return time_.ctime().replace(' ', '_').replace(':', '_'), time_


class MatchCrawler(Crawler):
    def __init__(self, robots_checker, config, save_htmls: bool = False):
        """
        TODO: make MatchCrawler more testable
        """
        super(MatchCrawler, self).__init__(robots_checker)
        self.config = json.load(open(config, "r", encoding='utf-8'))
        self.pull_time_string = create_timestring()
        self.save_htmls = save_htmls
        self.database = {}

    def crawl(self):
        for country in self.config["soccer"]:
            for league_link in self.config["soccer"][country]:
                print(f"---- LOGGING {league_link} -----")
                time.sleep(FRIENDLY_TIMER)
                self.check_allowed(league_link)
                request = requests.request("get", league_link)
                if self.save_htmls is True:
                    self.log_html(country, league_link, request)
                hrefs = self.find_hrefs(request.text)
                links = self.filter_hrefs(hrefs, league_link)
                if country not in self.database.keys():
                    self.database[country] = []
                self.database[country].extend(links)
        self.save_crawling_results()

    def log_html(self, country, league_link, request):
        html_filename = f"crawler/logs/{country}_{self.pull_time_string}_{league_link.split('/')[-2]}.html"
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(request.text)
        f.close()

    @staticmethod
    def find_hrefs(text):
        soup = BeautifulSoup(text, "html.parser")
        return soup.find_all('a', href=True)

    @staticmethod
    def filter_hrefs(hrefs, url):
        website = url.split(".com")[0] + ".com"
        base_extension = url.split(".com")[-1]
        links = []
        for a in hrefs:
            candidate = a["href"]
            if base_extension in candidate:
                if candidate.endswith(".html"):
                    if website + candidate not in links:
                        links.append(website + candidate)
        return links

    def save_crawling_results(self):
        json.dump(self.database,
                  open(f"crawler/matches/{self.pull_time_string}.json", "w", encoding="utf-8"),
                  indent=4,
                  sort_keys=True
                  )


class BetCrawler(Crawler):
    def __init__(self, robots_checker, bet_extractor, matchfile):
        """crawls bets and odds from the crawled matches """
        super(BetCrawler, self).__init__(robots_checker)
        self.match_links = json.load(open(matchfile, "r", encoding="utf-8"))
        self.pull_time_string, self.pull_time = self.create_timestring()
        self.current_link = None
        self.bet_extractor = bet_extractor

    def crawl(self):
        for matches in list(self.match_links.values()):
            for match in matches:
                print(f"------- PULLING {match} -------")
                time.sleep(FRIENDLY_TIMER)
                self.pull_time_string, self.pull_time = self.create_timestring()
                self.current_link = match
                self.check_allowed(match)
                request = requests.request("get", match)
                game_datetime = self.get_game_datetime(request.text)
                home_club, away_club = self.get_contesters(request.text)
                if self.has_started(game_datetime, self.pull_time):
                    print(f"Game {match} has already started. Skipping.")
                    continue
                odds = self.bet_extractor(match, request.text).crawl()
                if odds is not None:
                    filename = self.create_filename(home_club, away_club, game_datetime)
                    json.dump(odds, open(filename, "w", encoding="utf-8"), indent=4, sort_keys=True)
                # try:
                #     odds = self.extract_3_way_match_table(request.text)   #
                # except IndexError:   #
                #     print(f"Cannot crawl {match}")   #
                #     continue   #


    @staticmethod
    def has_started(game_time, pull_time):
        is_running_ = (datetime.strptime(game_time, '%d.%m.%Y %H:%M') - pull_time).total_seconds() <= 0
        return is_running_

    @staticmethod
    def get_contesters(content):
        soup = BeautifulSoup(content, "html.parser")
        findings = soup.find_all("span", itemprop="performers")
        home_club = findings[0].find_all("span", itemprop="name")[0].text
        away_club = findings[1].find_all("span", itemprop="name")[0].text
        return home_club, away_club

    @staticmethod
    def get_game_datetime(content):
        soup = BeautifulSoup(content, "html.parser")
        findings = soup.find_all("div", class_="uk-width-1-5 uk-text-center datetime")[0].text
        return re.findall(r"[0-9]{2}.[0-9]{2}.[0-9]{4} [0-9]{2}:[0-9]{2}", findings)[0]

    @staticmethod
    def create_filename(home_club, away_club, datetime):
        dt = datetime.replace(":", "_").replace(" ", "_").replace(".", "_")
        hc = home_club.replace(" ", "_")
        ac = away_club.replace(" ", "_")
        dirpath = "crawler/bets"
        return f"{dirpath}/{dt}_{hc}_{ac}.json"

# add Odds class
# class Odds:
#     def __init__(self, game, last_pull):
#         self.bookie = None
#         self.game = game
#         self.last_pull = last_pull
#         self.bookie_odds = {}
#
#     def add_bookie(self, bookie, odds):
#         self.bookie_odds[bookie] = odds
#
#     def create_filename(self): pass
#
#     def save(self):
#         saving = {"bookie": self.bookie, "game": self.game, "last_pull": self.last_pull, "bookies": self.bookie_odds}
#         json.dump(saving, open(filename, "w", encoding="utf-8"), indent=4, sort_keys=True)


class ThreeWayBetExtractor:
    def __init__(self, link, content):
        self.match_link = link
        self.soup = BeautifulSoup(content, "html.parser")
        self.pull_time_string = create_timestring()

    def crawl(self):
        try:
            odds = self.extract()
        except IndexError:
            odds = None
        return odds

    def extract(self):
        table = self.soup.find_all("div", class_="allodds")
        if len(table) > 1:
            RuntimeWarning(f"found more than one odd-table {self.match_link} weird.")
        try:
            table = table[0].find_all("tbody")[0]
        except IndexError:
            raise IndexError(f"did not find a table in soup\n{self.soup}")
        # TODO: replace dict with BaseBet-Class
        odds = {}
        odds["game"] = self.match_link
        odds["last_pull"] = self.pull_time_string
        odds["bookies"] = {}
        for row in table.find_all("tr"):
            bookie, information = self.get_bookie(row)
            home, draw, away = information
            if bookie == "":
                print(bookie)
            if "%" in home:
                print(home)
            odds["bookies"][bookie] = {
                "home": home,
                "draw": draw,
                "away": away
            }
        return odds

    @staticmethod
    def get_bookie(row):
        try:
            bookie = row.find_all("a", href=True)[1].text
        except IndexError:  # the name of the bookie is not important enough to throw away the whole match. Use None.
            bookie = "None"
        information = re.findall("\\n\d+\.\d+\\n", row.text, overlapped=True)
        information = [info.split("\n")[1] for info in information]
        return bookie, information
