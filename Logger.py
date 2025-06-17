import os

LOGFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "suspicious_domains.log")

class Logger(object):
    def __init__(self, print_logs: bool = False):
        self._print_logs = print_logs

    @property
    def print_logs(self) -> bool:
        return self._print_logs
    
    @print_logs.setter
    def print_logs(self, value:bool):
        if not isinstance(value, bool):
            raise TypeError("print_logs must be a bool")
        self._print_logs = value

    def _format(self, severity:int, domains:list[str], issuer:str):
        if severity > 200:
            criticity = "[HIGH]"
        elif severity > 100:
            criticity = "[MEDIUM]"
        else:
            criticity = "[LOW]"
        return "{} - {} - {}".format(criticity, ",".join(domains), issuer)


    # def alert(self, message: str):
    def alert(self, severity:int, domains:list[str], issuer:str):
        message = self._format(severity, domains, issuer)
        if self.print_logs:
            print(message)

        with open(LOGFILE, 'a') as f:
            f.write(f"{message}\n")
            

    def alert_db(self, severity:int, domains:list[str], issuer:str):
        raise NotImplementedError
    
    def alert_elastic(self,severity:int, domains:list[str], issuer:str):
        raise NotImplementedError