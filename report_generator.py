#!/usr/bin/env python

import json
import logging

from os import getcwd
from datetime import datetime
from subprocess import check_output
from utils import *

with open(str(getcwd()) + "/config.json") as config_file:
    config = json.load(config_file)

# Setup Logger
if config["logging_level"] == "debug":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Logging setup to Debug")

today = datetime.now()
last_month = str(today.month - 1 if today.month > 1 else 12)
last_month_year = str(today.year if today.month > 1 else today.year - 1)
logging.debug("Year Month set to: " + last_month_year + "-" + last_month)

def generate():
    # Summary
    cmd = ledger_base_cmd(config) + [
           "-b", format_date(last_month_year, last_month, "1"),
           "-e", format_date(last_month_year, last_month,  get_last_day(last_month)),
           "balance", "expenses"]
    logging.debug("cmd = " + " ".join(cmd))
    summary_output = check_output(cmd).decode()


    # Grocery Trend
    grocery_trend_cmd = monthly_trends(config,
                               "expenses:grocery",
                               config["reports"]["grocery-trend-months"])

    logging.debug("Grocery trend cmd: " + " ".join(grocery_trend_cmd))
    grocery_output = check_output(grocery_trend_cmd).decode()


    # Electricity Trends
    electricity_trend_cmd = monthly_trends(config,
                                           "utilities:electricity",
                                           config["reports"]["electricity-trend-months"])

    logging.debug("Electricity trend cmd: " + " ".join(electricity_trend_cmd))
    electricity_output = check_output(electricity_trend_cmd).decode()

    output = """<pre>
Summary
-------
%s

Grocery
-------
%s

Electricity
-----------
%s
</pre>""" % (summary_output, grocery_output, electricity_output)

    return output

if __name__ == "__main__":
    report = generate()
    print(report)
