import os
import sqlite3
from datetime import datetime

# TODO: typing
LOGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "suspicious_domains.log")


class Logger(object):
    def __init__(self, print_logs: bool = False, db_file: str | None = None):
        self.print_logs = print_logs
        self.db_file = db_file

    @property
    def print_logs(self) -> bool:
        return self._print_logs

    @print_logs.setter
    def print_logs(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("print_logs must be a bool")
        self._print_logs = value

    @property
    def db_file(self) -> str | None:
        return self._db_file

    @db_file.setter
    def db_file(self, value: str | None):
        if not isinstance(value, str) and value is not None:
            raise TypeError("db_file must be a dict or None")
        if value is not None:
            self._db_file = value
            self._db_connection = sqlite3.connect(value)

    @property
    def db_connection(self):
        return self._db_connection

    @db_connection.deleter
    def db_connection(self):
        self._db_connection.close()

    def _format_criticity(self, severity: int):
        if severity >= 200:
            criticity = "[HIGH]"
        elif severity >= 150:
            criticity = "[MEDIUM]"
        else:
            criticity = "[LOW]"
        return criticity

    def _format(self, severity: int, domains: list[str], issuer: str):
        return "{} {} {}".format(self._format_criticity(severity), ",".join(domains), issuer)

    def alert(self, severity: int, domains: list[str], issuer: str):
        message = self._format(severity, domains, issuer)
        if self.print_logs:
            print(message)

        with open(LOGFILE, "a") as f:
            f.write(f"{message}\n")

    def alert_db(self, severity: int, domains: list[str], issuer: str):
        cur = self._db_connection.cursor()
        for domain in domains:
            cur.execute(
                "INSERT INTO alerts (datetime, domain, criticity, issuer) VALUES (?,?,?,?)",
                (datetime.now().timestamp(), domain, self._format_criticity(severity), issuer),
            )
        self._db_connection.commit()
        cur.close()
