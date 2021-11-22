# Beat The Bookie Crawler

Read this paper to get to know the method https://arxiv.org/abs/1710.02824. This repo should not be used for real money
betting. I never tested it enough for that. Use it for fun paper-betting. Use of this repo is always on your own risk.
Also give the authors of the original paper some appreciation: https://github.com/Lisandro79/BeatTheBookie


# Disclaimer
This repository contains code and further links that one can use to get suggestions for a betting strategy.
If you are sports betting and decide to test the strategy or use it on real betting, bear in mind that you are doing it 
under your own risk and responsibility. 
I do not claim any responsiblity for: A) the use that you might make of the code, 
B) the information you find here or 
C) any monetary losses you might incur during your betting experience.


## How can this work?
The outcome of a sports event might be considered a random event, where the result is realized in the exact moment the referee calls it off. Consider a football match a 90 minutes long toincoss, where heads, tails and side have some fixed probability of outcome once the game has started. You toss the coin and just wait 90 minutes for the real result to realize. The bookies will not only beat you in being much more precise than you (which they are nevertheless), but also because the probabilities of the match outcomes are playing against you. Consider this example:
| /                      | Home | Draw | Away |
|------------------------|------|------|------|
| Probability of Winning | 1/2  | 1/4  | 1/4  |
| "Fair" Odds            | 2    | 4    | 4    |
| Real Odds              | 1.9  | 3.8  | 3.8  |

The home team has a 50% chance of winning, however the bookie is just giving you 1.9 times the return. It's a 25% Chance of a draw, however the bookie is just giving you 3.8 times your money back if you win. Same goes for a win of the away-team. So - hypothetically speaking - if you'd know the "real" probabilities in advance, you still could not make any money from this game, because the odds are just made that way, that you lose in the long run. Going back to the coinflip: Lets say heads is 49%, tails is 49%, and the coin landing on the side is just 2%. The odds for this game would be something like: H:1.9, T:1.9, S:20, which has the underlying probabilities of 52%, 52%, 5% of making money for the bookie. You can add this up and you'll end up ad 109%, or speaking in different terms: The bookie will win 9% of your money each turn on average. Same goes for the football example.

Now, when you're trying to beat the bookie, you have to think like a bookie. First you'll extract the mean winning probabilities for each game by averaging the odds over a lot of bookies. That's really easy, you can use a crawler for that. Search for a bookie that has misplaced it's odds. It doesn't matter for which team he has misplaced the odds or if you think the team he mislpaced the odds for will win or lose. Remember that its just a random event that will realize its result once the ref calls the game off. 


## Description
- I guess one could get the necessary information by registering at some websites, but I wanted to do something on my own to be able to implement my own solutions
- Implementation of a crawler to get the necessary data this paper https://arxiv.org/abs/1710.02824
- Basically leverage the spread between multiple bookies
- makes heavy usage of this website: https://www.wettportal.com/
- THIS REPOSITORY IS NOT MEANT TO BE USED FOR REAL-MONEY BETTING

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
