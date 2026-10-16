import json
import hmac
import tkinter as tk
import os
import uuid
from secrets import token_bytes



# ----------------------------
# CONFIG
# ----------------------------
TEMP_DIR = os.path.join("Data","Logs","tmp_crypto")


# ----------------------------
# SECURE KEY WRAPPER
# ----------------------------
class SecureKey:
    def __init__(self, key_bytes: bytes):
        self._key = bytearray(key_bytes)

    def __enter__(self):
        return self

    def get(self):
        return bytes(self._key)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._key:
            for i in range(len(self._key)):
                self._key[i] = 0
            self._key = None


# ----------------------------
# KEY MANAGEMENT
# ----------------------------
def create_key(path: str):
    key = token_bytes(32)

    with open(path, "wb") as f:
        f.write(key)

    del key


def get_key(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


