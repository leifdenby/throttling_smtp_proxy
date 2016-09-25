from __future__ import absolute_import

import smtplib
import os
import socket
import sys

from base.celery import app

SES_USERNAME = os.environ.get('SES_USERNAME')
SES_PASSWORD = os.environ.get('SES_PASSWORD')
SES_HOSTNAME = os.environ.get('SES_HOSTNAME', "email-smtp.us-east-1.amazonaws.com")
SES_RATE_LIMIT = os.environ.get("SES_RATE_LIMI", "5/s")

if SES_USERNAME is None or SES_PASSWORD is None:
    raise Exception("Error: please set the SES_USERNAME and SES_PASSWORD env variables")

@app.task(rate_limit=SES_RATE_LIMIT)
def send_email(mailfrom, rcpttos, data):
    refused = {}
    try:
        s = smtplib.SMTP()
        s.connect(SES_HOSTNAME, port=587)
        s.starttls()
        s.login(SES_USERNAME, SES_PASSWORD)

        try:
            refused = s.sendmail(mailfrom, rcpttos, data)
        finally:
            s.quit()
    except smtplib.SMTPRecipientsRefused as e:
        print('got SMTPRecipientsRefused')
        refused = e.recipients
    except (socket.error, smtplib.SMTPException) as e:
        print(DEBUGSTREAM, 'got', e.__class__)
        # All recipients were refused.  If the exception had an associated
        # error code, use it.  Otherwise,fake it with a non-triggering
        # exception code.
        errcode = getattr(e, 'smtp_code', -1)
        errmsg = getattr(e, 'smtp_error', 'ignore')
        for r in rcpttos:
            refused[r] = (errcode, errmsg)

    if len(refused) != 0:
        print(refused)
    else:
        print("Successfully sent email to `{}`".format(str(rcpttos)))

    # TODO: do something with errors here
