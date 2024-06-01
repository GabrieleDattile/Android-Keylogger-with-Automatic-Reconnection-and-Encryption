import base64
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return base64.b64encode(encrypted_data)

def decrypt(data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(base64.b64decode(data))
    return decrypted_data.decode()

# Esempio di generazione chiave (non dovresti rigenerarla ogni volta)
key = generate_key()
