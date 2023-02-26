import os
import pickle

class actor:
    def __init__(self, phone_number):
        self.phone = phone_number
        self.path = f'users/{phone_number}.pkl'
        self.prev_msgs = []

    def save_msg(self, msg):
        self.prev_msgs.append(msg)

    def save(self):
        with open(self.path, 'wb') as data:
            pickle.dump(self, data)
