import jwt
import _datetime


class Token:
    __SECRET = 'password'
    __ALGO = 'HS256'

    # in minutes
    __SESSION_TIME = 3

    def __init__(self, token_str: str):

        try:
            self.__token = jwt.decode(str.encode(token_str), Token.__SECRET, Token.__ALGO)
            self.__valid = True
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            self.__valid = False

    def is_valid(self):
        return self.__valid

    @staticmethod
    def generate_token_str(user_name: str):
        return jwt.encode({
                'username': user_name,
                'exp': _datetime.datetime.utcnow() + _datetime.timedelta(minutes=Token.__SESSION_TIME)
            },
            Token.__SECRET,
            algorithm=Token.__ALGO
        ).decode('utf-8')

    def extract_user_name(self):
        return self.__token['username']
