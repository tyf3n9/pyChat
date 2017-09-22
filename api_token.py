import json


class Token:
    def __init__(self, username: str):
        self.username = username

    def get_token(self):
        return json.dumps({'username': self.username})

    @staticmethod
    def extract_user_name(token: str):
        obj = json.loads(token)

        try:
            return obj['username']
        except KeyError:
            return None

    @staticmethod
    def validate(token: str):
        obj = json.loads(token)

        try:
            return obj['username'] == obj['username']
        except KeyError:
            return False
