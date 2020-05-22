import json

class Message:
    def __init__(self, src, dest, body):
        self.src = src
        self.dest = dest
        self.body = body

    @staticmethod
    def from_json(text):
        parsed = json.loads(text)
        return Message(parsed['src'], parsed['dest'], parsed['body'])

    def to_json(self):
        return json.dumps({
            'src': self.src,
            'dest': self.dest,
            'body': self.body
        })
