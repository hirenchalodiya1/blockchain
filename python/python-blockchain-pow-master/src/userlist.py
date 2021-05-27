from tinydb import TinyDB, Query


class UserList:
    def __init__(self):
        self.users = TinyDB('users.json')

    def __str__(self):
        users_as_list = []
        for username in self.users.keys():
            user = self.users[username]
            users_as_list.append(user.__str__())
        return users_as_list.__str__()

    def add_user(self, user):
        User = Query()
        if self.users.search(User.username == user.username):
            return "Username already exists"
        self.users.insert({
            'name': user.name,
            'username': user.username,
            'email_id': user.email_id,
            'public_key': user.public_key
        })
        return "Success"

    def get_user(self, username):
        User = Query()
        result = self.users.search(User.username == username)
        if not result:
            return "Username does not exist"
        return result[0]
