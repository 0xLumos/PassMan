import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets





class EncryptedPasswordManager:
    
    def __init__(self, master_password):
        self.master_password = master_password.encode()
        self.key = hashlib.pbkdf2_hmac('sha256', self.master_password, b'salt', 100000)
        print(self.key)
        self.aesgcm = AESGCM(self.key)
        self.passwords = []

    def add_password(self, website, username, password):
        website_nonce = secrets.token_bytes(16)  # Generate a random 16-byte (i.e. 128-bit) nonce
        username_nonce = secrets.token_bytes(16)
        password_nonce = secrets.token_bytes(16)
        website_encrypted = self.aesgcm.encrypt(nonce=website_nonce, data=website.encode(), associated_data=None)
        username_encrypted = self.aesgcm.encrypt(nonce=username_nonce, data=username.encode(), associated_data=None)
        password_encrypted = self.aesgcm.encrypt(nonce=password_nonce, data=password.encode(), associated_data=None)
        encrypted_data = (website_nonce + website_encrypted, username_nonce + username_encrypted, password_nonce + password_encrypted)
        self.passwords.append(encrypted_data)
        print("Password added successfully!")
        print(self.passwords)
        return (website, username, password)
     

    def get_password(self, website, username):
        for website_data, username_data, password_data in self.passwords:
            website_nonce, website_encrypted = website_data[:16], website_data[16:]
            username_nonce, username_encrypted = username_data[:16], username_data[16:]

            if website_encrypted == self.aesgcm.encrypt(nonce=website_nonce, data=website.encode(), associated_data=None) and \
                username_encrypted == self.aesgcm.encrypt(nonce=username_nonce, data=username.encode(), associated_data=None):
                password_nonce, password_encrypted = password_data[:16], password_data[16:]
                decrypted_password = self.aesgcm.decrypt(data=password_encrypted, nonce=password_nonce, associated_data=None)
               
                return decrypted_password.decode()





