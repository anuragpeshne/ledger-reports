#!/usr/bin/env python

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
import json
import report_generator

from os import getcwd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

with open(str(getcwd()) + "/config.json") as config_file:
    config = json.load(config_file)

report = report_generator.generate()

message = Mail(
    from_email='anurag.peshne@gmail.com',
    to_emails='anurag.peshne@gmail.com',
    subject='Expense Times',
    html_content=report)
try:
    sg = SendGridAPIClient(config["sendgrid"]["token"])
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)
