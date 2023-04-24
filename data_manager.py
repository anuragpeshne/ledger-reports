#!/usr/bin/env python3

import json
import logging

from os import getcwd
from subprocess import check_output
from utils import *

DELIMITER = "---"

with open(str(getcwd()) + "/config.json") as config_file:
    config = json.load(config_file)

# Setup Logger
if config["logging_level"] == "debug":
    #logging.basicConfig(level=logging.DEBUG)
    logging.debug("Logging setup to Debug")

# Given a month and a year, returns a list of account and amount sorted by amount
def get_monthly_expenses(year, month):
    cmd = ledger_base_cmd(config) + [
            "-b", format_date(year, month, "1"),
            "-e", format_date(year, month, get_last_day(month)),
            "balance", "expenses", "--no-total", "--flat",
            "--format", "%(amount)" + DELIMITER + "%(account)\n"]
    output = check_output(cmd).decode()
    parsed_data = []
    for row in output.split('\n'):
        if row:
            amount, acc = row.split(DELIMITER)
            acc = clear_prefix(acc, "Expenses")
            amount = convert_currency_to_float(amount)
            parsed_data.append((amount, acc))
    parsed_data = sorted(parsed_data, key=lambda amt_acc: amt_acc[0],
                         reverse=True)
    return parsed_data

def get_trend_expenses(last_month_year, term, years_to_compare=3):
    start_year = int(last_month_year) - years_to_compare + 1
    yearly_data = {}
    for year in range(start_year, int(last_month_year) + 1):
        cmd = ledger_base_cmd(config) + ["register",
                                         term,
                                         "--no-total",
                                         "--flat",
                                         "--monthly",
                                         "--begin", str(year),
                                         "--end", str(year + 1),
                                         "--format",
                                         DELIMITER.join(["%(date)", "%t\n"])]
        output = check_output(cmd).decode()
        group_by_month = [0] * 12
        for row in output.split('\n'):
            if not row:
                continue
            rowsplit = row.split(DELIMITER)
            if len(rowsplit) == 1:
                # handle cases in which multiple currencies were used in a
                # single transactions later.
                continue
            date, amount = rowsplit
            _, month, _ = date.split("/")
            group_by_month[int(month) - 1] += round(
                    convert_currency_to_float(amount))
        yearly_data[year] = group_by_month
    return yearly_data
