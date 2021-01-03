
class RobotsTxtError(Exception):
    def __init__(self, website):
        """ throw this if the robots.txt does not allow to crawl a website you wanted."""
        self.website = website
        super().__init__(self.website)

    def __str__(self):
        return f'cannot crawl {self.website}'
