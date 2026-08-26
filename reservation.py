import uuid

class Reservation:
    def __init__(self, user, slot):
        self.id = uuid.uuid4()
        self.user = user
        self.slot = slot
        self.status = "Active"