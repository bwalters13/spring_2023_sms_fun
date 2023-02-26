import os
import pickle
from flask import request, g
from classes.Actor import Actor
from tools.config import yml_configs
from bin.handle_input import handle_input

def load_actor(phone_number: str) -> Actor:
    actor = None
    path = f'users/{phone_number}.pkl'

    if os.exists(path):
        with os.open(path, 'rb') as data:
            actor = pickle.load(data)
    else:
        actor = Actor(phone_number)

    return actor

def handle_request():
    phone_number = request.form['From']

    actor = load_actor(phone_number)

    input_msg = request.form['Body']
    output_msg = handle_input(actor, input_msg)

    g.sms_client.messages.create(
        body = output_msg,
        from_ = yml_configs['twilio']['phone_number'],
        to = request.form['From'])
    
    actor.save_msg(input_msg)
    actor.save()

    return "OK", 200