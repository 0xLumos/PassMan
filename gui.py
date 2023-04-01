import tkinter as tk
from tkinter import ttk
from security import EncryptedPasswordManager

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
        self.password_manager = EncryptedPasswordManager("mysecretpassword")

        # Add pages to the dictionary
        for F in (HomePage, AboutPage, ContactPage, LoginPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self, password_manager=self.password_manager)
            self.frames[page_name] = frame

            # Place the frame in the container
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the home page initially
        self.show_frame("HomePage")

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
        username_entry = tk.Entry(self)
        username_entry.pack(pady=5)

        # Create password label and entry
        password_label = tk.Label(self, text="Password:")
        password_label.pack(pady=5)
        password_entry = tk.Entry(self, show="*")
        password_entry.pack(pady=5)

        # Create login button
        login_button = tk.Button(self, text="Login", command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.pack(pady=5)

    def login(self, username, password):
        # Add your login logic here
        print(f"Logging in with username '{username}' and password '{password}'")

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






