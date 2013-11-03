# -*- coding: utf-8 -*-

import requests
import hashlib
import json

from settings import OVH_APP_KEY, OVH_CONSUMER_KEY, OVH_SECRET_KEY
from settings import RECIPIENTS, SENDER, OVH_SERVICE_NAME

OVH_SEND_URL = "https://api.ovh.com/1.0/sms/%s/jobs"
OVH_TIME_URL = 'https://api.ovh.com/1.0/auth/time'

# default SMS params, should work in most cases.
DEFAULT_SMS_PARAMS = {
    'class': "phoneDisplay",
    'coding': "7bit",
    'noStopClause': True,
    'priority': "high",
    'validityPeriod': '2880'
}


class OvhSmsSenderException(Exception):

    def __init__(self, msg=None, response=None):

        super(OvhSmsSenderException, self).__init__()
        self.response = response
        self.msg = msg

    def __str__(self):

        res = ""
        if self.msg:
            res += self.msg
        if self.response:
            for k, v in self.response.json().iteritems():
                res += "\n%s: %s" % (k, v)
        return res


class OvhSmsSender(object):
    ''' based on https://www.ovh.com/fr/g934.premiers-pas-avec-l-api '''

    def __init__(
            self, app_key=OVH_APP_KEY, secret_key=OVH_SECRET_KEY,
            consumer_key=OVH_CONSUMER_KEY, service_name=OVH_SERVICE_NAME,
            **kwargs):

        if not app_key or not secret_key or not consumer_key \
                or not service_name:
            raise OvhSmsSenderException(
                msg='Missings parameters. Check settings.py.')

        self.app_key = app_key
        self.consumer_key = consumer_key
        self.secret_key = secret_key
        self.send_url = OVH_SEND_URL % service_name

        self.msg_headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            'X-Ovh-Application': app_key,
            'X-Ovh-Consumer': consumer_key,
        }

        self.msg_params = DEFAULT_SMS_PARAMS

        # Useful for to overloading params
        for key in kwargs:
            self.msg_params[key] = kwargs[key]

    def send_msg(self, msg, sender=SENDER, recipients=RECIPIENTS):

        # API request payload
        self.msg_params['message'] = msg
        self.msg_params['sender'] = sender
        self.msg_params['receivers'] = recipients
        data = json.dumps(self.msg_params)

        # API request timestamp
        timestamp = str(int(requests.get(OVH_TIME_URL).text))

        # API request signing
        signature = hashlib.sha1()
        signature.update("+".join([
            self.secret_key, self.consumer_key, 'POST',
            self.send_url, data, timestamp]))
        signature = "$1$" + signature.hexdigest()

        # API request headers
        self.msg_headers.update({
            'X-Ovh-Timestamp': timestamp,
            "X-Ovh-Signature": signature})

        response = requests.post(
            self.send_url, data=data, headers=self.msg_headers)

        if response.status_code != 200:
            raise OvhSmsSenderException(
                msg="Sending failed", response=response)
