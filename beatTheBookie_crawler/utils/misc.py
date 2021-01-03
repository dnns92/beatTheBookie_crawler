from datetime import datetime


def create_timestring():
    return datetime.now().ctime().replace(' ', '_').replace(':', '_')
