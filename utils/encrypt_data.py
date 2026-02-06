import hashlib

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

from config import get_settings

settings = get_settings()

AES_KEY = hashlib.sha256(settings.aes_key.encode()).digest()
FIXED_IV = settings.fixed_IV


def encrypt(data: str) -> str:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(FIXED_IV))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(ct).decode()


def decrypt(data: str) -> str:
    encrypted_bytes = base64.b64decode(data)
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(FIXED_IV))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_bytes) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return (unpadder.update(padded_data) + unpadder.finalize()).decode()
