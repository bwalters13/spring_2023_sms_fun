from twilio.rest import Client
from flask import g

sms_client = None

def get_sms_client():
    global sms_client

    sms_client = Client(g.secrets['twilio_account'], g.secrets['twilio_token'])

    return sms_client