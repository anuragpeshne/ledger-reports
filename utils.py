from datetime import datetime

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

def monthly_trends(config, target, duration):
    start = int(last_month) - duration
    start_month = start if start > 0 else 12 + start
    start_year = last_month_year if start > 0 else last_month_year - 1

    trend_cmd = ledger_base_cmd(config) + [
            "-b", format_date(start_year, start_month, "1"),
            "-e", format_date(last_month_year, last_month,  get_last_day(last_month)),
            "register", target,
            "--monthly"]
    return trend_cmd
