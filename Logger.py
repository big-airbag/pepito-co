import os

LOGFILE = "{}/suspicious_domains.log".format(os.path.dirname(os.path.abspath(__file__)))


def Logger(object):
    def __init__(self, print_logs: bool = False):
        raise NotImplementedError

    def alert(self, message: str):
        raise NotImplementedError
