class Message:
    def __init__(self, payload):
        self.drop_box_id = None
        self.message_payload = payload

    def set_drop_box_id(self, id):
        self.drop_box_id = id

    def get_drop_box_id(self):
        return self.drop_box_id

