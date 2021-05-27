import json
from tinydb import TinyDB

POOL_DIR = 'data/common'


class Message:
    def __init__(self, username, name, msg, timestamp):
        self.sender_username = username
        self.sender_name = name
        self.msg = msg
        self.timestamp = timestamp

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True)


class MessageList:
    def __init__(self):
        self.messages = TinyDB(POOL_DIR + 'pool.json')

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True)

    def add(self, message):
        self.messages[message.timestamp] = message
        return "Success"
