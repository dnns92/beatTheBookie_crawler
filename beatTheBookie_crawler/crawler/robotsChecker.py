import urllib.robotparser

from beatTheBookie_crawler.crawler.crawler_constants import ROBOTSTXT


class WettPortalComRobotsChecker:
    def __init__(self):
        """small wrapper to read the https://www.wettportal.com/robots.txt """
        self.parser = urllib.robotparser.RobotFileParser()
        self.parser.set_url(ROBOTSTXT)

    def can_fetch(self, website):
        self.parser.read()
        allowed_all = self.parser.can_fetch("*", website)
        allowed_me = self.parser.can_fetch("beatTheBookie_crawler", website)
        return allowed_all and allowed_me
