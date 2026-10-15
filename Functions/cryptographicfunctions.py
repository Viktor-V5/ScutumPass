import json
import hmac
import tkinter as tk
import os
import uuid
from Crypto.Cipher import AES
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


# ----------------------------
# TEMP FILE HANDLING
# ----------------------------
def _ensure_temp_dir():
    os.makedirs(TEMP_DIR, exist_ok=True)


def _temp_file_path():
    return os.path.join(TEMP_DIR, f"enc_{uuid.uuid4().hex}.tmp")


def atomic_write(file_path: str, data: bytes):

    _ensure_temp_dir()

    temp_path = _temp_file_path()

    with open(temp_path, "wb") as f:
        f.write(data)

    os.replace(temp_path, file_path)

    #os.remove(temp_path)


def encrypt_file(file_path: str, key: bytes):

    if not isinstance(key, (bytes, bytearray)) or len(key) != 32:
        raise ValueError("Key must be 32 bytes (AES-256)")
        
    with open(file_path, "rb") as f:
        data = f.read()

    nonce = token_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    ciphertext, tag = cipher.encrypt_and_digest(data)

    atomic_write(file_path, nonce + tag + ciphertext)

def decrypt_file(file_path: str, key: bytes) -> bytes:

    if not isinstance(key, (bytes, bytearray)) or len(key) != 32:
        raise ValueError("Key must be 32 bytes (AES-256)")

    with open(file_path, "rb") as f:
        nonce = f.read(12)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


def change_key(old_key_bytes: bytes, file_target: str, account_type: str,account_id: str):

    # ----------------------------
    # Validate old key
    # ----------------------------
    if not isinstance(old_key_bytes, (bytes, bytearray)):
        raise ValueError("Key must be bytes")

    if len(old_key_bytes) != 32:
        raise ValueError("Invalid AES-256 key length")

    # ----------------------------
    # Select new key location
    # ----------------------------
    new_key_location = tk.filedialog.asksaveasfilename(
        defaultextension=".key",
        initialdir="/",
        title="Select location for the new key",
        filetypes=[("Key file", "*.key")]
    )

    if not new_key_location:
        raise ValueError("No file selected for new key")

    # ----------------------------
    # Create new key
    # ----------------------------
    create_key(new_key_location)

    if os.name != "nt":
        os.chmod(new_key_location, 0o600)

    new_key_bytes = get_key(new_key_location)

    if len(new_key_bytes) != 32:
        raise ValueError("Generated key is invalid")

    # ----------------------------
    # Decrypt existing file
    # ----------------------------
    try:
        plaintext = decrypt_file(file_target, old_key_bytes)
        data = json.loads(plaintext.decode("utf-8"))
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ValueError(
            "Failed to decrypt file (wrong key or corrupted file)"
        ) from e

   
    # ----------------------------
    # Build deterministic payload
    # ----------------------------
    payload = {
        field: data[field]
        for field in required_fields
    }

    payload_bytes = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")

    # ----------------------------
    # Generate NEW HMAC
    # ----------------------------
    new_hmac = hmac_sha256(
        new_key_bytes,
        payload_bytes
    )

    # ----------------------------
    # Re-encrypt using PLAINTEXT
    # ----------------------------
    with open(file_target, "wb") as f:
        f.write(plaintext)

    encrypt_file(
        file_target,
        new_key_bytes
    )

    # ----------------------------
    # Verify
    # ----------------------------
    try:
        verify_plaintext = decrypt_file(
            file_target,
            new_key_bytes
        )

        json.loads(
            verify_plaintext.decode("utf-8")
        )

    except Exception as e:
        raise RuntimeError(
            "Re-encryption verification failed"
        ) from e

    # ----------------------------
    # Success
    # ----------------------------
    tk.messagebox.showinfo(
        "Success",
        "Key rotation completed successfully."
    )

    return True
