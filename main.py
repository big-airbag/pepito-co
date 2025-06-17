import argparse
import sys
from AbuseIPDBClient import AbuseIPDBClient
from BaseApiClient import BaseApiClient
from Logger import Logger
import certstream
from Levenshtein import distance
import configparser
import os
import json

config = configparser.ConfigParser()
# TODO: if file do not exist, create it with base parameter
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
config.read("config.ini")

ABUSEIPDB_API_KEY = config["DEFAULT"]["AbuseIPDB_API_Key"]
BASE_DISTANCE_KEYWORD = config["DEFAULT"]["Base_Distance_Keyword"]
DISTANCE_THRESHOLD = int(config["DEFAULT"]["Distance_Threshold"])


def on_open():
    print("Connection successfully established!")


def main(args: argparse.Namespace):
    def my_callback(message, context):
        # Skip some messages
        if (
            message["message_type"] == "heartbeat"
            or message["data"]["update_type"] == "PrecertLogEntry"
            or len(message["data"]["leaf_cert"]["all_domains"]) == 0
        ):
            return

        if message["message_type"] == "certificate_update":
            global_score = 0

            # Parse message
            issuer = message["data"]["leaf_cert"]["issuer"]
            domains = message["data"]["leaf_cert"]["all_domains"]

            # 1 : Compute distance
            for domain in domains:
                d = distance(BASE_DISTANCE_KEYWORD, domain)
                if d <= DISTANCE_THRESHOLD:
                    # score = 100 if d == 1; as d increase, score decrease
                    global_score += round((len(BASE_DISTANCE_KEYWORD) - d) * 100 / (len(BASE_DISTANCE_KEYWORD) - 1))

                    # 2 : Test issuer
                    if issuer["O"] == "Let's Encrypt":
                        global_score += 50

                    # 3 : AbuseIPDB
                    score = aipdb_client.check_reputation(domain=domain)
                    global_score += score

                    # 4 : Logging
                    if global_score > 100:
                        logger.alert(severity=global_score, domains=domains, issuer=issuer["aggregated"])
                        # Break to test the next certificate without duplicating
                        # alerts for other domains in this one
                        break

    aipdb_client = AbuseIPDBClient(api_key=ABUSEIPDB_API_KEY)
    logger = Logger(print_logs=args.print_logs)

    certstream.listen_for_events(my_callback, on_open=on_open, url="ws://localhost:4000/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Tool I-Tracing", description="Search for typosquatting certificates")
    parser.add_argument("--print-logs", action="store_true", help="If a suspicious domain is logged, print it")
    parser.add_argument(
        "--debug", action="store_true", help="Debug mode, increase tolerance in search for similar URLs"
    )
    args = parser.parse_args()

    if args.debug:
        print("****** WARNING ******")
        print("In debug mod, a lot of domain may be analysed and a significant API usage can ensue")
        print("Be sure that the Base Distance Keyword is also good")
        DISTANCE_THRESHOLD = 7

    main(args)
