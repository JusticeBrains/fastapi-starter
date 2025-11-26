import bcrypt


class Hasher:
    def __init__(self):
        self._salt = bcrypt.gensalt()

    def hash(self, password: str):
        return bcrypt.hashpw(password.encode("utf-8"), salt=self._salt)

    def verify(self, password: str, hashed_password: bytes):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
