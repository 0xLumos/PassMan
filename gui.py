import tkinter as tk
from tkinter import ttk
from security import EncryptedPasswordManager
from tkinter import messagebox
import rsa
import base64
from cryptography.hazmat.primitives import serialization
class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1900x700")
        self.title("PassMan")
        # Create a container to hold the different pages
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand=True)
        container
        # Create a dictionary to hold the different pages
        self.frames = {}

        # Create an instance of the password manager class
        self.password_manager = EncryptedPasswordManager()

        # Add pages to the dictionary
        for F in (HomePage, AboutPage, ContactPage, LoginPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self, password_manager=self.password_manager)
            self.frames[page_name] = frame

            # Place the frame in the container
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the home page initially
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        # Show the given frame
        frame = self.frames[page_name]
        frame.tkraise()


class AddPasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        website_label = tk.Label(self, text="Website:")
        website_label.pack(pady=5)
        website_entry = tk.Entry(self)
        website_entry.pack(pady=5)
        
        username_label = tk.Label(self, text="Username:")
        username_label.pack(pady=5)
        username_entry = tk.Entry(self)
        username_entry.pack(pady=5)
        
        password_label = tk.Label(self, text="Password:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(self, show="*")
        password_entry.pack(pady=5)
        
        add_button = tk.Button(self, text="Add", command=lambda: self.add_password(website_entry.get(), username_entry.get(), password_entry.get()))
        add_button.pack(pady=2)
    
    def add_password(self, website, username, password):
        # Add the password to the password manager
        password_data = self.controller.password_manager.add_password(website, username, password)

        # Insert the new password data into the table
        #self.controller.frames["HomePage"].table.insert("", tk.END, values=password_data)
        
        # Destroy the current frame
        self.master.destroy()


class HomePage(tk.Frame):
    def __init__(self, parent, controller, password_manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.password_manager = password_manager

        label = tk.Label(self, text="Home Page")
        label.pack(side="top", fill="x", pady=10)
        
        # Create the table
        self.table = ttk.Treeview(self, columns=("website", "username", "password"), show="headings")
        self.table.pack(padx=650, pady=60)
        self.table.heading("website", text="Website")
        self.table.heading("username", text="Username")
        self.table.heading("password", text="Password")
        
        # Create the add password button
        add_password_button = tk.Button(self, text="Add Password", command=self.open_add_password_page)
        add_password_button.pack(pady=5)

        # Create the about and contact buttons
        button1 = tk.Button(self, text="About", command=lambda: controller.show_frame("AboutPage"))
        button2 = tk.Button(self, text="Contact", command=lambda: controller.show_frame("ContactPage"))
        button1.pack()
        button2.pack()
    
    def open_add_password_page(self):
        add_password_window = tk.Toplevel(self)
        add_password_window.title("Add Password")
        add_password_window.geometry("600x400")
        add_password_window.resizable(False, False)

        add_password_page = AddPasswordPage(add_password_window, self.controller)
        add_password_page.pack(fill="both", expand=True)




class LoginPage(tk.Frame):

    def __init__(self, parent, controller, password_manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.password_manager = password_manager

        # Create username label and entry
        username_label = tk.Label(self, text="Username:")
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        # Create password label and entry
        password_label = tk.Label(self, text="Password:")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # Create login button
        login_button = tk.Button(self, text="Login", command=lambda: self.login(self.username_entry.get()))
        login_button.pack(pady=5)
        
        # Create generate key pair button
        generate_key_button = tk.Button(self, text="Generate Key Pair", command=self.generate_key_pair)
        generate_key_button.pack(pady=5)

    def generate_key_pair(self):
        self.private_key, self.public_key = self.password_manager.generate_key_pair()
        print(self.private_key)
        print(self.public_key)
        print(self.username_entry.get())
        username = self.username_entry.get()
        public_key = self.password_manager.get_public_key(username)
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
        print(public_key_bytes.decode('utf-8'))
        print(self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))


    def login(self, username):
        if username == "":
             messagebox.showerror("Error", "Please provide a username")
             return
        # Get the user's public key from the password manager
        public_key = self.password_manager.get_public_key(username)
        print(self.public_key)
        if not public_key:
            messagebox.showerror("Error", "User not found")
            return

        # Decrypt the user's password using their private key
        password = self.password_manager.decrypt_password(self.password_entry.get(), self.private_key)

        # Verify the password using the user's public key
        # you should use a lambda function to wrap the self.login method call to delay the execution of the method until the button is clicked.
        # The lambda function returns a function object, and in this case, it wraps the self.login method 
        # and passes the self.username_entry.get() value as an argument to the method when the button is clicked. This is done to avoid the method being called immediately upon creating the LoginPage object.
        if not self.password_manager.verify_password(username, password, public_key):
            messagebox.showerror("Error", "Incorrect password")
            return

        # Switch to the home page
        self.controller.show_frame("HomePage")



class AboutPage(tk.Frame):

    def __init__(self, parent, controller, password_manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.password_manager = password_manager

        label = tk.Label(self, text="About Page")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        button.pack()

class ContactPage(tk.Frame):

    def __init__(self, parent, controller, password_manager):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.password_manager = password_manager

        label = tk.Label(self, text="Contact Page")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        button.pack()






