from functools import reduce
from hashlib import sha1
from json import dumps, loads
from binascii import hexlify, unhexlify
from .pyaes import AESModeOfOperationCTR

class Helper:
    def __init__(self):
        pass

    @staticmethod
    def hash(data):
        return sha1(data.encode("utf-8")).hexdigest()

    @staticmethod
    def readable(data):
        return reduce(lambda a, b: a + chr(int(b, 16) + 103), list(data))

    @staticmethod
    def JSONEncoding(data):
        return dumps(data)

    @staticmethod
    def JSONDecoding(data):
        return loads(data)

    @staticmethod
    def bytesToHex(bytes):
        return hexlify(bytes).decode()

    @staticmethod
    def hexToBytes(hex):
        return unhexlify(hex.encode())

    @staticmethod
    def encrypt(data, key):
        aes = AESModeOfOperationCTR(key)
        ciphertext = aes.encrypt(data)
        return Helper.bytesToHex(ciphertext)
        # return hexlify(ciphertext).decode()

    @staticmethod
    def decrypt(ciphertext, key):
        aes = AESModeOfOperationCTR(key)
        # data = unhexlify(ciphertext.encode())
        data = Helper.hexToBytes(ciphertext)
        return aes.decrypt(data)
