from functools import reduce
from hashlib import sha1
from json import dumps, loads
from binascii import hexlify, unhexlify
from .pyaes import AESModeOfOperationCTR

class Cipher:
    @staticmethod
    def advancedEncryption(data, key):
        aes = AESModeOfOperationCTR(key)
        ciphertext = aes.encrypt(data)
        return Helper.bytesToHex(ciphertext)

    @staticmethod
    def advancedDecryption(ciphertext, key):
        aes = AESModeOfOperationCTR(key)
        data = Helper.hexToBytes(ciphertext)
        return aes.decrypt(data)

    @staticmethod
    def xor(data, key):
        return "".join([ chr(ord(ciphertextA) ^ ord(ciphertextB)) for (ciphertextA, ciphertextB) in zip(data, key) ])

    @staticmethod
    def simpleEncyption(data, key):
        ciphertext = Cipher.xor(data, key).encode("utf-8")
        return Helper.bytesToHex(ciphertext)

    @staticmethod
    def simpleDecryption(ciphertext, key):
        ciphertext = Helper.hexToBytes(ciphertext)
        return Cipher.xor(ciphertext.decode("utf-8"), key)

class Helper:
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

    Cipher = Cipher
