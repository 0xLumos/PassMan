from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import secrets
import hashlib
import cryptography
class EncryptedPasswordManager:
    def __init__(self):

        self.passwords = []
        self.private_key, self.public_key = self.generate_key_pair()

    def add_password(self, website, username, password):
        website_nonce = secrets.token_bytes(16)
        username_nonce = secrets.token_bytes(16)
        password_nonce = secrets.token_bytes(16)
        website_encrypted = self.public_key.encrypt(website.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        username_encrypted = self.public_key.encrypt(username.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        password_encrypted = self.public_key.encrypt(password.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        encrypted_data = (website_encrypted, username_encrypted, password_encrypted)
        self.passwords.append(encrypted_data)
        print("Password added successfully!")
        print(self.passwords)
        return (website, username, password)
    

    def get_public_key(self,username):
        return self.public_key
    

    def get_password(self, website, username):
        for website_data, username_data, password_data in self.passwords:
            website_decrypted = self.private_key.decrypt(website_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
            username_decrypted = self.private_key.decrypt(username_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
            if website_decrypted == website.encode() and username_decrypted == username.encode():
                password_decrypted = self.private_key.decrypt(password_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
                return password_decrypted.decode()

    def generate_key_pair(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return private_key, public_key
