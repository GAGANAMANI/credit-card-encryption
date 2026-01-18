import os
import json
import uuid
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import secrets

# Load encryption key from environment variable
KEY = os.getenv("CARD_KEY")

if not KEY or len(KEY) != 32:
    raise ValueError("CARD_KEY must be set to a 32-character value")

def mask_pan(pan):
    return "**** **** **** " + pan[-4:]

def encrypt_pan(pan):
    iv = secrets.token_bytes(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(pan.encode()) + padder.finalize()

    cipher = Cipher(
        algorithms.AES(KEY.encode()),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    return iv.hex() + ":" + encrypted.hex()

def tokenize_pan(encrypted_pan):
    token = str(uuid.uuid4())
    record = {
        "token": token,
        "encrypted_pan": encrypted_pan
    }

    with open("token_store.json", "a") as f:
        f.write(json.dumps(record) + "\n")

    return token

if __name__ == "__main__":
    print("CREDIT CARD ENCRYPTION SYSTEM (EDUCATIONAL)")
    pan = input("Enter dummy credit card number: ")

    masked = mask_pan(pan)
    encrypted = encrypt_pan(pan)
    token = tokenize_pan(encrypted)

    print("\nMasked PAN:", masked)
    print("Generated Token:", token)
    print("Encrypted PAN stored securely")
