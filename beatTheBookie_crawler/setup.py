import os


def check_dirs(iter_):
    for i in iter_:
        if not os.path.exists(i):
            os.mkdir(i)


if __name__ == '__main__':
    base_dir = os.getcwd()
    crawler_dir = os.path.join(base_dir, "crawler")
    bet_dir = os.path.join("crawler", "bets")
    match_dir = os.path.join("crawler", "matches")
    profitable_dir = os.path.join("crawler", "profitables")
    check_dirs([crawler_dir, bet_dir, match_dir, profitable_dir])

    with open("dirs.py", "w") as f:
        f.write(f"BET_DIR = '{bet_dir}'\n")
        f.write(f"MATCH_DIR = '{match_dir}'\n")
        f.write(f"PROFITABLE_DIR = '{profitable_dir}'\n")
    f.close()
