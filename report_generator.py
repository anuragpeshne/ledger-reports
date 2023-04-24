#!/usr/bin/env python

import json
import logging

from os import getcwd
from datetime import datetime
from matplot_charts import make_pie_chart, make_line_chart_monthly_trends
from data_manager import get_monthly_expenses, get_trend_expenses
from subprocess import check_output
from utils import *

DELIMITER = "---"

with open(str(getcwd()) + "/config.json") as config_file:
    config = json.load(config_file)

# Setup Logger
if config["logging_level"] == "debug":
    #logging.basicConfig(level=logging.DEBUG)
    logging.debug("Logging setup to Debug")

today = datetime.now()
last_month = str(today.month - 1 if today.month > 1 else 12)
last_month_year = str(today.year if today.month > 1 else today.year - 1)
logging.debug("Year Month set to: " + last_month_year + "-" + last_month)

def expense_summary_chart():
    parsed_data = get_monthly_expenses(last_month_year, last_month)
    chart = make_pie_chart(parsed_data)

    table_content = []
    for amount, acc in parsed_data:
        table_content.append("<tr>")
        table_content.append(
                "<td style=\"text-align:right\">{:.2f}</td>".format(amount))
        table_content.append("<td style=\"text-align:left\">" + acc + "</td>")
        table_content.append("</tr>")
    chart_div = """
<div style="width:900px; font-family:monospace">
    <div style="float:left;width:60%%">
        <img src="data:image/png;base64,%s" />
    </div>
    <div style="float:right;width:40%%;">
    <table>
        %s
    </table>
    </div>
</div>
""" % (chart, ''.join(table_content))
    return chart_div

def trends_chart(term, years_to_compare=3):
    yearly_data = get_trend_expenses(last_month_year, term, years_to_compare)
    chart = make_line_chart_monthly_trends(yearly_data, term)
    chart_div = """
<div style="width=900px; font-family:monospace">
    <div> <img src="data:image/png;base64,%s" /> </div>
    <pre>%s</pre>
</div>
""" % (chart, '\n'.join([str(yearly_data[year]) for year in yearly_data]))
    return chart_div

def generate_html():
    html = []
    html.append(expense_summary_chart())
    html.append(trends_chart("^Expenses"))
    html.append(trends_chart("^Expenses:Utilities:Electricity"))
    html.append(trends_chart("^Expenses:Grocery"))
    html.append(trends_chart("^Expenses:Shopping"))
    return '\n'.join(html)

def generate_text():
    # Summary
    cmd = ledger_base_cmd(config) + [
           "-b", format_date(last_month_year, last_month, "1"),
           "-e", format_date(last_month_year, last_month,
                             get_last_day(last_month)),
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
    #report = generate_text()
    report = generate_html()
    print(report)
