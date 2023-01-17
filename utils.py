from datetime import datetime
import re

today = datetime.now()
last_month = today.month - 1 if today.month > 1 else 12
last_month_year = today.year if today.month > 1 else today.year - 1

def format_date(year=None, month=None, day=None):
    today = datetime.now()
    year = today.year if not year else year
    month = today.month if not month else month
    day = today.day if not day else day

    return "%s-%s-%s" % (year, month, day)

def get_last_day(month):
    return 30 if int(month) in [2, 4, 6, 9, 11] else 31

def ledger_base_cmd(config):
    return ["ledger", "-f", config["ledger"]["file-location"]]

# Returns command for monthly trends.
# `start_year` can be supplied for historical comparison or is calculated based
# on whether current - duration takes us back to the last year.
def monthly_trends(config, target, duration, year=last_month_year):
    start = int(last_month) - duration
    start_month = start if start > 0 else 12 + start
    start_year = year if start > 0 else year - 1

    trend_cmd = ledger_base_cmd(config) + [
            "-b", format_date(start_year, start_month, "1"),
            "-e", format_date(last_month_year, last_month,
                              get_last_day(last_month)),
            "register", target,
            "--monthly"]
    return trend_cmd

# Remove prefix from Ledger account.
# Example: clear_prefix("Expenses:Utilities:Electricity", "Expenses") ->
# "Utilities:Electricity"
def clear_prefix(val, prefix):
    val = val.split(':')
    if val[0] == prefix:
        val = val[1:]

    return ':'.join(val)

# Extracts currency value
# Example: convert_currency_to_float("$2,000") -> 2000.00
def convert_currency_to_float(amount):
    amount = amount.replace(',', '')
    other_currency = False
    if not amount.startswith('$'):
        _, other_currency = amount.split(' ')
    m = re.match(".([\-\.\d]+)", amount)
    if not other_currency:
        # if dollar return amount
        return float(m.group(1))
    # convert to dollar
    if other_currency == "INR":
        return float(m.group(1)) / 80
    raise "Unknown currency: " + other_currency
