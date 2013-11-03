ovh_sms_sender
==============

Simple SMS sender via OVH API.


Requirements
------------

* python-requests


Settings.py
-----------

You'll need a SMS account with credits in ovh.com

> OVH_SERVICE_NAME = "sms-XXYYYYY-Z"

Credentials
More info here: https://www.ovh.com/fr/g934.premiers-pas-avec-l-api

> OVH_APP_KEY = "xxxxxxxxxxx"
> OVH_SECRET_KEY = "yyyyyyyyyy"
> OVH_CONSUMER_KEY = "zzzzzzzzzz"

Default sender must be registered in the OVH SMS Panel. Can be a phone number 
or name.

> SENDER = '+33abcdefg'


Usage
-----

> import ovh_sms_sender
> sender = ovh_sms_sender.OvhSmsSender()
> sender.send_msg('Hello world', recipients=['+33abcde'])

