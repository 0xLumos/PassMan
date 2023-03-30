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
