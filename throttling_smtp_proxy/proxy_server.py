import smtpd
import asyncore

import base.tasks

class ThrottledProxy(smtpd.PureProxy):
    def _deliver(self, mailfrom, rcpttos, data):
        base.tasks.send_email.delay(mailfrom=mailfrom, rcpttos=rcpttos, data=data)

server = ThrottledProxy(('0.0.0.0', 1025), ('127.0.0.1', 1026))

asyncore.loop()
