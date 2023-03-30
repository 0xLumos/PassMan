import hashlib


class EncryptedPasswordManager:
    
    def __init__(self, master_password):
        self.master_password = master_password.encode()
        self.key = hashlib.pbkdf2_hmac('sha256', self.master_password, b'salt', 100000)
        print(self.key)
        self.aesgcm = AESGCM(self.key)
        self.passwords = []

    





