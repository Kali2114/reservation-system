from threading import Lock


class User:
    id = 1
    lock = Lock()
    def __init__(self, name, email):
        with User.lock:
            self.id = User.id
            User.id += 1
        self.name = name
        self.email = email
