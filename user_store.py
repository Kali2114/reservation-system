from user import User
from security import hash_password, verify_password


class UserStore:
    def __init__(self):
        self.users = {}

    def register(self, name, email, password):
        if email in self.users:
            raise ValueError('email already registered')
        salt, hashed_password = hash_password(password)
        new_user = User(name, email, hashed_password, salt)
        self.users[email] = new_user
        return new_user

    def login(self, email, password):
        if email not in self.users:
            raise ValueError('invalid email or password')
        user = self.users[email]
        if not verify_password(password, user.salt, user.password_hash):
            raise ValueError('invalid email or password')
        return user


