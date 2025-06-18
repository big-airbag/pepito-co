# Technical challenge
This repository holds source code for a technical challenge.

## Compatibility
This tool is tested in Python3.12 and python3.13.

## :heavy_plus_sign: Requirements
A functional [Certstream Server](https://github.com/CaliDog/certstream-server). Its websocket URL will be used in the config file (see below).

## :wrench: Initialization
- Install python requirements :
```
python3 -m venv my-venv/
source my-venv/bin/activate
pip3 install -r requirements.txt
```

- Now you can launch the main program :
```
python3 main.py
```
It will create a blank config file (config.ini) and exit.

- Create a .db file somewhere, initialize it with the provided SQL script and fill the config file.
```
sqlite3 YOUR_FILEPATH
sqlite> .read db/init.sql
```

Now you're ready to go.


## :white_check_mark: Testing
You can test the code with pytest :
```
python3 -m pytest -vvv
```

## Usage
```
usage: Tool I-Tracing [-h] [--print-logs] [--debug] [--to-db]

Search for typosquatting certificates

options:
  -h, --help    show this help message and exit
  --print-logs  If a suspicious domain is logged, print it
  --debug       Debug mode, increase tolerance in search for similar URLs
  --to-db       Log alerts to a db file
```
Example :
```
python3 main.py --debug --print-logs
```

You can read results in the auto-generated log file : suspicious_domains.log or in the database if configured.