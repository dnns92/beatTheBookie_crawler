import os
import re
import shutil
import time
from datetime import datetime
from glob import glob

from beatTheBookie_crawler.crawler.crawler_constants import VERY_FRIENDLY_TIMER, HISTORY_DIR, CANDIDATE_DIR


class PastGamesFilter:
    def __init__(self, root, interval=VERY_FRIENDLY_TIMER):
        """ put this into a new process using a function wrapper """
        self.root = root
        self.files = None
        self.history_dir = HISTORY_DIR
        self.timer = interval
        self.get_files()

    def get_files(self):
        self.files = glob(os.path.join(self.root, "*.json"))

    def run(self):
        self.get_files()
        now = datetime.now()
        for file in self.files:
            if self.has_started(file, now):
                filename = os.path.basename(file)
                shutil.move(file, os.path.join(self.root, self.history_dir, filename))

    def run_continuous(self):
        while True:
            time.sleep(self.timer)
            self.run()

    @staticmethod
    def has_started(filename, now):
        date_time = re.findall("\d{2}_\d{2}_\d{4}_\d{2}_\d{2}", filename)[0]
        return (datetime.strptime(date_time, '%d_%m_%Y_%H_%M') - now).total_seconds() < 0

