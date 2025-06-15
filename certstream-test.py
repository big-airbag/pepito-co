import logging
import sys
import datetime
import certstream
import ssl

def print_callback(message, context):
    logging.debug("Message -> {}".format(message))

    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        if len(all_domains) == 0:
            domain = "NULL"
        else:
            domain = all_domains[0]

        sys.stdout.write(u"[{}] {} (SAN: {})\n".format(datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S'), 
                                                       domain, 
                                                       ", ".join(message['data']['leaf_cert']['all_domains'][1:])))
        sys.stdout.flush()

def on_open():
    print("Connection successfully established!")

def on_error(instance, exception):
    # Instance is the CertStreamClient instance that barfed
    print("Exception in CertStreamClient! -> {}".format(exception)) 

logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.DEBUG)

certstream.listen_for_events(message_callback=print_callback, on_open=on_open, on_error=on_error, url='wss://certstream.calidog.io/')
