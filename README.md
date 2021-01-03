# Beat The Bookie Crawler

Read this paper to get to know the method https://arxiv.org/abs/1710.02824

## Description
- I guess one could get the necessary information by registering at some websites, but I wanted to do something on my own to be able to implement my own solutions
- Implementation of a crawler to get the necessary data this paper https://arxiv.org/abs/1710.02824
- Basically leverage the spread between multiple bookies
- makes heavy usage of this website: https://www.wettportal.com/

## Installation
    git clone <this>
    cd <this>
    cd crawler/
    mkdir matches logs bets profitables
    cd bets
    mkdir history
    conda create -y -n <your_env_name>
    conda activate <your_env_name>
    conda install python=3.8*
    pip install requests
    pip install regex  # new regex module

## Usage

Be nice and always check for the robots.txt.

--- DO NOT DELETE THE FRIENDLY TIMERS TO PREVENT PUTTING LOAD ON THE TARGET WEBSITE ---

In my case, I use a raspberry pi to crawl new games once per day and evaluate the games as well on it.

- Use the MatchCrawler to crawl upcoming matches and save those to matches/*.json
- Use the BetCrawler to crawl the odds from the bookies for each match
- It should tell you about btb-strategy candidate games and also create a profitables/ folder


## Roadmap

- [ ] Crawl more bets independent of the game type and bet type (currently you can only crawl soccer  + home, away, draw bets)
- [ ] Make crawlers more testable
- [ ] Extract a Class to guess the expected value
- [ ] Implement a pytorch-model to guess the expected value
- [ ] Implement a Telegram Bot that can notify the user on btb-strategy candidates
- [ ] Implement a surebet-finder
- [ ] Replace json file-handling with a sql-database
