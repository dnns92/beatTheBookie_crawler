from beatTheBookie_crawler.crawler.crawler_constants import ROBOTSTXT
from datetime import datetime
import time
import urllib.robotparser


def sleep_hours(hours):
    time.sleep(hours*60*60)


def sleep_minutes(minutes):
    time.sleep(minutes*60)


if __name__ == '__main__':
    # it should be sufficient to crawl once per day
    new_day = True
    while True:
        now = datetime.now()
