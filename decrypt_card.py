import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

KEY = os.getenv("CARD_KEY")

if not KEY or len(KEY) != 32:
    raise ValueError("CARD_KEY must be set to a 32-character value")

def decrypt_pan(encrypted_data):
    iv_hex, enc_hex = encrypted_data.split(":")
    iv = bytes.fromhex(iv_hex)
    encrypted = bytes.fromhex(enc_hex)

    cipher = Cipher(
        algorithms.AES(KEY.encode()),
        modes.CBC(iv),
        backend=default_backend()
    )

    decryptor = cipher.decryptor()
    padded = decryptor.update(encrypted) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    pan = unpadder.update(padded) + unpadder.finalize()

    return pan.decode()

if __name__ == "__main__":
    encrypted_pan = input("Enter encrypted PAN: ")
    print("Decrypted PAN:", decrypt_pan(encrypted_pan))
