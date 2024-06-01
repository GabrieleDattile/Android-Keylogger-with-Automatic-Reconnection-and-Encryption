import base64
import os
from hashlib import pbkdf2_hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def generate_key(password):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key, salt

def authenticate(password, key, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    stored_key = base64.urlsafe_b64encode(kdf.derive(password))
    return stored_key == key

def generate_auth_token(key):
    f = Fernet(key)
    token = f.encrypt(b'authenticated')
    return token

def authenticate_token(token, key):
    f = Fernet(key)
    try:
        f.decrypt(token)
        return True
    except Exception:
        return False
