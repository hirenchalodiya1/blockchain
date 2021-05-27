import json


class User:
    def __init__(self, name, username, email_id, public_key):
        self.name = name
        self.username = username
        self.email_id = email_id
        self.public_key = public_key

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True)
