from threading import Lock


class User:
    id = 1
    lock = Lock()
    def __init__(self, name, email, password_hash=None, salt=None):
        with User.lock:
            self.id = User.id
            User.id += 1
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.salt = salt
