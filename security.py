from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import secrets
import hashlib
import cryptography
import glob
class EncryptedPasswordManager:
    def __init__(self):

        self.passwords = []
        self.private_key, self.mem_public_key = self.generate_key_pair()

    def add_password(self, website, username, password):

        website_encrypted = self.mem_public_key.encrypt(website.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        username_encrypted = self.mem_public_key.encrypt(username.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        password_encrypted = self.mem_public_key.encrypt(password.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        encrypted_data = (website_encrypted, username_encrypted, password_encrypted)
        self.passwords.append(encrypted_data)
        print("Password added successfully!")
        print(self.passwords)
        return (website, username, password)
    

    def get_mem_public_key(self,username):
        return self.mem_public_key
    

    def get_password(self, website, username):
        for website_data, username_data, password_data in self.passwords:
            website_decrypted = self.private_key.decrypt(website_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
            username_decrypted = self.private_key.decrypt(username_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
            if website_decrypted == website.encode() and username_decrypted == username.encode():
                password_decrypted = self.private_key.decrypt(password_data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
                return password_decrypted.decode()

    def generate_key_pair(self):
        mem_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        mem_public_key = mem_private_key.public_key()
        private_key = mem_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key = mem_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
        # print(public_key_bytes.decode('utf-8'))
        print(private_key)
        f = open("passman_id.rsa", "a")
        f.write(str(private_key))
        f.close()  
        f = open("passman_id_pub.rsa", "a")
        f.write(str(public_key))
        f.close() 
        return mem_private_key, mem_public_key
    
    def find_keys(self):
        keys_files = glob.glob('**/*.rsa', recursive=True)
        if len(keys_files) < 2:
            print("missing key file/s")
            return False
        else:
            print("Keys Found")
            return True
