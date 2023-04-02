from security import EncryptedPasswordManager

from gui import GUI

from storage import MerkleTree


if __name__ == "__main__":
    master_password = 'mysecretpassword'
    private_key = None
    # Create an instance of the EncryptedPasswordManager
    password_manager = EncryptedPasswordManager()

    # Add a new password
    website = 'www.example.com'
    username = 'myusername'
    password = 'MyVeryStrongPassword'
    password_manager.add_password(website, username, password)
    


    # Get a password
    retrieved_password = password_manager.get_password(website, username)
    print(f"Retrieved password: {retrieved_password}")
    app = GUI()

   
    app.mainloop()
