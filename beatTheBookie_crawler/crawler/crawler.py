import json
import time
import requests
from datetime import datetime
from glob import glob
import os

import regex as re
from bs4 import BeautifulSoup

from beatTheBookie_crawler.utils.robots import RobotsTxtError
from .crawler_constants import FRIENDLY_TIMER, Result
from beatTheBookie_crawler.utils.misc import create_timestring


class Crawler:
    def __init__(self, robots_checker=None):
        """Base Class for MatchCrawler and BetCrawler
        TODO: implement more functionality here and less in the specific crawlers"""
        self.robots_checker = robots_checker
        self.pull_time_string, self.pull_time = self.create_timestring()

    def check_allowed(self, link):
        allowed = self.robots_checker.can_fetch(link)
        if not allowed:
            raise RobotsTxtError(link)

    @staticmethod
    def create_timestring():
        time_ = datetime.now()
        return time_.ctime().replace(' ', '_').replace(':', '_'), time_


class MatchCrawler(Crawler):
    def __init__(self, robots_checker, config, save_htmls: bool=False, return_filename=False):
        """
        TODO: make MatchCrawler more testable
        """
        super(MatchCrawler, self).__init__(robots_checker)
        self.config = json.load(open(config, "r", encoding='utf-8'))
        self.save_htmls = save_htmls
        self.return_filename = return_filename
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
        filename = self.save_crawling_results()
        if self.return_filename is True:
            return filename

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
        filename = f"crawler/matches/{self.pull_time_string}.json"
        json.dump(self.database,
                  open(filename, "w", encoding="utf-8"),
                  indent=4,
                  sort_keys=True
                  )
        return filename


class BetCrawler(Crawler):
    def __init__(self, robots_checker, bet_extractor, matchfile):
        """crawls bets and odds from the crawled matches """
        super(BetCrawler, self).__init__(robots_checker)
        self.match_links = json.load(open(matchfile, "r", encoding="utf-8"))
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


class ResultCrawler(Crawler):
    def __init__(self, robots_checker, base_dir, target_dir):
        super(ResultCrawler, self).__init__(robots_checker)
        self.base_dir = base_dir
        self.target_dir = target_dir
        self.files = glob(os.path.join(base_dir, "*.json"))

    def crawl(self):
        for file in self.files:
            print(f"--- READING {file} ---")
            profitable = json.load(open(file, "r", encoding='utf-8'))
            for game_link in profitable:
                time.sleep(FRIENDLY_TIMER)
                self.check_allowed(game_link)
                request = requests.request("get", game_link)
                soup = BeautifulSoup(request.text, "html.parser")
                if self.check_has_ended(soup):
                    score = self.get_score(soup)
                    profitable[game_link]["best_odds"]["score"] = score
                    filename = f"{self.target_dir}/results_{self.pull_time_string}.json"
                    json.dump(profitable,
                              open(filename, "w", encoding="utf-8"),
                              indent=4,
                              sort_keys=True
                              )

    @staticmethod
    def check_has_ended(soup):
        minute = soup.find_all("span", class_="minute")
        if minute:
            if minute[0] == "Beendet":
                return True
        return False

    @staticmethod
    def get_score(soup):
        result = soup.find_all("span", class_="score")
        home, away = result[0].split(":")
        home, away = int(home), int(away)
        return Result.eval_score(home, away)


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
