import os


def check_dirs(iter_):
    for i in iter_:
        if not os.path.exists(i):
            os.mkdir(i)


if __name__ == '__main__':
    base_dir = os.getcwd()
    crawler_dir = os.path.join(base_dir, "crawler")
    bet_dir = os.path.join(crawler_dir, "bets")
    match_dir = os.path.join(crawler_dir, "matches")
    profitable_dir = os.path.join(crawler_dir, "profitables")
    paperbet_dir = os.path.join(crawler_dir, "paperbet")
    log_dir = os.path.join(crawler_dir, "logs")
    check_dirs([crawler_dir, bet_dir, match_dir, profitable_dir, paperbet_dir, log_dir])

    with open("dirs.py", "w") as f:
        f.write(f"CRAWLER_DIR = '{crawler_dir}'\n")
        f.write(f"BET_DIR = '{bet_dir}'\n")
        f.write(f"MATCH_DIR = '{match_dir}'\n")
        f.write(f"PROFITABLE_DIR = '{profitable_dir}'\n")
        f.write(f"PAPERBET_DIR = '{paperbet_dir}'\n")
        f.write(f"LOG_DIR = '{log_dir}'\n")
    f.close()
