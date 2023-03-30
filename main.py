from encrypt_decrypt import EncryptedPasswordManager

from gui import GUI


if __name__ == "__main__":
    master_password = 'mysecretpassword'

    # Create an instance of the EncryptedPasswordManager
    password_manager = EncryptedPasswordManager(master_password)

    # Add a new password
    website = 'www.example.com'
    username = 'myusername'
    password = 'MyVeryStrongPassword'
    password_manager.add_password(website, username, password)



    # Get a password
    retrieved_password = password_manager.get_password(website, username)
    print(f"Retrieved password: {retrieved_password}")
    app = GUI()
    app.geometry("1900x700")
    app.title("PassMan")
   
    app.mainloop()
