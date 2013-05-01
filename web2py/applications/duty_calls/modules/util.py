from gluon import *
from twilio.rest import TwilioRestClient
import os
import json

request = current.request
conf_path = os.path.join(request.folder,'private','conf.json')
with open(conf_path,'r') as f:
    conf = json.load(f)
    os.environ['TWILIO_AUTH_TOKEN'] = conf['TWILIO_AUTH_TOKEN']
    os.environ['TWILIO_ACCOUNT_SID'] = conf['TWILIO_ACCOUNT_SID']

twilio_client = TwilioRestClient()

def getTwilioNumber(twilio_number_id):
    return twilio_client.phone_numbers.get(twilio_number_id).friendly_name
