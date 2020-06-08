import json
import struct
import datetime
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

def datetime_from_ms(ms):
    dt = datetime.datetime.fromtimestamp(ms // 1000)
    return datetime.datetime(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            1000 *(ms % 1000))


def datetime_to_ms(dt):
    return int(1000 * dt.timestamp())


class PeerMessage:
    def __init__(self, message, deaddrop, send_time=None):
        self.message = message
        self.deaddrop = deaddrop
        self.send_time = send_time or datetime.datetime.now()

    @classmethod
    def _from_bytes(cls, b, peer_ec_key):
        signature = b[0:72]

        # Remove padding from 72 byte field, to variable-length DER
        signature = signature[:signature[1] + 2]

        try:
            peer_ec_key.verify(signature, b[72:], ec.ECDSA(hashes.SHA256()))
        except InvalidSignature:
            print("Invalid signature: skipping")
            return None

        send_time = struct.unpack('<q', b[72:79] + b'\0')[0]
        send_time = datetime_from_ms(send_time)

        message_length = min(b[79], 160)
        message = b[80:80+message_length]
        message = message.decode()

        deaddrop = struct.unpack('<i', b[80+160:80+160+4])[0]

        return PeerMessage(message, deaddrop, send_time)

    @classmethod
    def from_encrypted_bytes(cls, b, peer_ec_key, aes_key):
        assert len(b) == 256 + 16

        iv = b[:16]
        decryptor = Cipher(aes_key, CBC(iv), default_backend()).decryptor()

        decrypted = decryptor.update(b[16:])
        decrypted += decryptor.finalize()

        return cls._from_bytes(decrypted, peer_ec_key)

    def _to_bytes(self, ec_key):
        assert len(self.message) <= 160

        send_time = datetime_to_ms(self.send_time)
        send_time = struct.pack('<q', send_time)[:7]

        message_length = bytes([len(self.message)])

        message = self.message.encode().ljust(160, b'\0')

        deaddrop = struct.pack('<i', self.deaddrop)
        deaddrop += b'\0' * 12 # padding

        b = send_time + message_length + message + deaddrop

        signature = ec_key.sign(b, ec.ECDSA(hashes.SHA256())).ljust(72, b'\0')

        return signature + b

    def to_encrypted_bytes(self, ec_key, aes_key):
        iv = os.urandom(16)
        encryptor = Cipher(aes_key, CBC(iv), default_backend()).encryptor()

        b_encrypted = iv
        b_encrypted += encryptor.update(self._to_bytes(ec_key))
        b_encrypted += encryptor.finalize()

        return b_encrypted


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
