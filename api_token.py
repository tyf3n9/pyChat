import jwt
import _datetime


class Token:
    __SECRET = 'password'
    __ALGO = 'HS256'

    # in minutes
    SESSION_TIME = 3
    LONG_SESSION_TIME = 60

    def __init__(self, token_str: str) -> None:

        try:
            self.__token = jwt.decode(str.encode(token_str), Token.__SECRET, Token.__ALGO)
            self.__valid = True
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            self.__valid = False

    def is_valid(self) -> bool:
        return self.__valid

    @staticmethod
    def generate_token_str(user_name: str, session_time: int) -> str:
        return jwt.encode({
                'username': user_name,
                'exp': _datetime.datetime.utcnow() + _datetime.timedelta(minutes=session_time)
            },
            Token.__SECRET,
            algorithm=Token.__ALGO
        ).decode('utf-8')

    def extract_user_name(self) -> str:
        if self.is_valid():
            return self.__token['username']
        else:
            return ''
