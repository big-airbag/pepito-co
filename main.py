from AbuseIPDBClient import AbuseIPDBClient
from BaseClient import BaseClient
import Logger
import certstream
from Levenshtein import distance
import configparser
import os
import json

config = configparser.ConfigParser()
#TODO: if file do not exist, create it with base parameter
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
config.read("config.ini")

ABUSEIPDB_API_KEY = config["DEFAULT"]["AbuseIPDB_API_Key"]
BASE_DISTANCE_KEYWORD = config["DEFAULT"]["Base_Distance_Keyword"]

def score_from_distance(s: str):
    return 100 - distance(BASE_DISTANCE_KEYWORD, s) * 20



def main():
   BaseClient("myurl")
   pass
    #### 1 distance


    #### 2 is from LetsEncrypt ?


    #### AbuseIPDB

    #### If suspicious => logging


    # aip = AbuseIPDBClient(api_key=ABUSEIPDB_API_KEY)
    # x = aip.check_reputation(ip="45.134.26.79")
    # print(x)

    # def my_callback(message, context): 
    #     # print(f"[LOG] {message}") 
    # certstream.listen_for_events(my_callback, url='ws://localhost:4000/')
    # bc = BaseClient(base_url="http://google.com")
    # bc.http_request("GET")


    

if __name__ == "__main__":
    print(os.path.join(os.path.dirname(os.path.abspath(__file__)), "suspicious_domains.log"))

    main()
