# SMTP Proxy with send rate throttle

This utility was written to be run as as a proxy between for example a postfix
smtp-server and Amazon SES, so that the rate limits of SES can be matched.

Two processes must be run: 1) the proxy smpt itself (will run on port 1025) and
2) a celery work to consume the send queue.

Set up by defining the Amazon SES username and password as env variables:

    > export SES_USERNAME='AKIAJZZ7MVSPQD2WCL22'
    > export SES_PASSWORD='AsZ56O3SG7NcOLQ3rRc+Dz/nnY53WwYbdTSEKKm3UTuu' 

Optionally the SES hostname and send rate can be defined too

    > export SES_HOSTNAME="email-smtp.us-east-1.amazonaws.com"
    > export SES_RATE_LIMIT="10/s"

Then change into the project root and run the two process:

    > git clone https://github.com/leifdenby/throttling_smtp_proxy
    > cd throttling_smtp_proxy
    > celery -A base worker
    > python proxy_server.py
