import tkinter as tk
from tkinter import ttk
class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
     
        # Create a container to hold the different pages
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand=True)
        container
        # Create a dictionary to hold the different pages
        self.frames = {}

        # Add pages to the dictionary
        for F in (HomePage, AboutPage, ContactPage, LoginPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Place the frame in the container
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the home page initially
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        # Show the given frame
        frame = self.frames[page_name]
        frame.tkraise()

def add_password(self):
    website = self.website_entry.get()
    username = self.username_entry.get()
    password = self.password_entry.get()

    password_data = self.password_manager.add_password(website, username, password)
    self.table.insert("", tk.END, values=password_data)
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Home Page")
        label.pack(side="top", fill="x", pady=10)
        
        # Create the table
        table = ttk.Treeview(self, columns=("website", "username", "password"), show="headings")
        table.pack(padx=650, pady=60)
        table.heading("website", text="Website")
        table.heading("username", text="Username")
        table.heading("password", text="Password")
        table.pack()

        # Insert some data into the table
        table.insert("", "end", values=("Facebook.com", "MyUserName", "MyPassword"))
        table.insert("", "end", values=("Instagram.com", "MyUserName", "MySecondPassword"))
        table.insert("", "end", values=("LinkedIn.com", "MyUserName", "MyThirdPassword"))
        

        button1 = tk.Button(self, text="About", command=lambda: controller.show_frame("AboutPage"))
        button2 = tk.Button(self, text="Contact", command=lambda: controller.show_frame("ContactPage"))
        button1.pack()
        button2.pack()




class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="About Page")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        button.pack()

class ContactPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Contact Page")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Home", command=lambda: controller.show_frame("HomePage"))
        button.pack()


