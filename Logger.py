import os
import sqlite3
from datetime import datetime

LOGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "suspicious_domains.log")


class Logger:
    """
    Custom Logger
    """

    def __init__(self, print_logs: bool = False, db_file: str | None = None):
        """Initialize logger with parameters

        Args:
            print_logs (bool, optional): Activate log printing. Defaults to False.
            db_file (str | None, optional): A path to a sqlite3 database file. Defaults to None.
        """
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
    def db_connection(self) -> sqlite3.Connection:
        return self._db_connection

    @db_connection.deleter
    def db_connection(self):
        self._db_connection.close()

    def _format_criticity(self, severity: int) -> str:
        """Format criticity given a severity score

        Args:
            severity (int): Severity score

        Returns:
            str: criticity formatted
        """
        if severity >= 200:
            criticity = "[HIGH]"
        elif severity >= 150:
            criticity = "[MEDIUM]"
        else:
            criticity = "[LOW]"
        return criticity

    def _format(self, severity: int, domains: list[str], issuer: str) -> str:
        """Format a log

        Args:
            severity (int): Severity score
            domains (list[str]): A list of web domains
            issuer (str): Certificate issuer

        Returns:
            str: Custom log formatted
        """
        return "{} {} {}".format(self._format_criticity(severity), ",".join(domains), issuer)

    def alert(self, severity: int, domains: list[str], issuer: str):
        """Log an alert in a logfile

        Args:
            severity (int): Severity score
            domains (list[str]): A list of web domains
            issuer (str): Certificate issuer
        """
        message = self._format(severity, domains, issuer)
        if self.print_logs:
            print(message)

        with open(LOGFILE, "a") as f:
            f.write(f"{message}\n")

    def alert_db(self, severity: int, domains: list[str], issuer: str):
        """Log an alert in the database

        Args:
            severity (int): Severity score
            domains (list[str]): a list of web domains
            issuer (str): Certificate issuer

        Raises:
            Exception: Method called but class instance has no db_file attribute
        """
        if self.db_file is None:
            raise Exception("Called alert_db method but db_file is None")

        cur = self._db_connection.cursor()
        for domain in domains:
            cur.execute(
                "INSERT INTO alerts (datetime, domain, criticity, issuer) VALUES (?,?,?,?)",
                (datetime.now().timestamp(), domain, self._format_criticity(severity), issuer),
            )
        self._db_connection.commit()
        cur.close()
