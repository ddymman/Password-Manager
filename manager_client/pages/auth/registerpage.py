import tkinter as tk
import hashlib
import os
from PIL import Image, ImageTk
import json

from manager_client.pages.page import Page
from manager_client.pages.router import Router
from manager_client.pages.route import Route
from manager_client.network.client import Client
from manager_network.register import RegisterMessage, RegisterResponseCode
from manager_client.data.appdata import AppData, Account
import manager_client.utils.config as config

class RegisterPage(Page):
    def __init__(self, root: tk.Tk, router: Router, client: Client, appdata: AppData):
        Page.__init__(self, root, router, client, appdata)

        self.img = Image.open("assets/logo.png")
        self.img = ImageTk.PhotoImage(self.img.resize((300, 300)))

        self.input_frame = tk.Frame(self)
        self.login_var = tk.StringVar()
        self.login_entry = None
        self.password_var = tk.StringVar()
        self.password_entry = None
        self.button_frame = tk.Frame(self)
        self.register_button = None
        self.back_button = None
        self.register_result_text = tk.StringVar()
        self.register_result = None


    def render(self):
        self.grid_columnconfigure((0, 1, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)

        canvas = tk.Canvas(self, width=300, height=300)
        canvas.create_image(0, 0, image=self.img, anchor="nw")
        canvas.grid(row=0, column=1)

        tk.Label(self,
                 text="=---------------------            Register            ---------------------=",
                 font=("Calibri", 18)
                 ).grid(row=1, column=1, pady=20)

        self.input_frame = tk.Frame(self)

        self.input_frame.grid_columnconfigure((0, 1), weight=1)
        self.input_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)

        tk.Label(self.input_frame, text="Username: ", font=("Calibri", 14)).grid(row=0, column=0)

        self.login_var = tk.StringVar()
        self.login_entry = tk.Entry(self.input_frame,
                                    textvariable=self.login_var,
                                    width=30,
                                    font=("Calibri", 14))
        self.login_entry.grid(row=0, column=1)

        tk.Label(self.input_frame, text="Password: ", font=("Calibri", 14)).grid(row=1, column=0, pady=5)

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self.input_frame,
                                       textvariable=self.password_var,
                                       width=30,
                                       show="*",
                                       font=("Calibri", 14))
        self.password_entry.grid(row=1, column=1)

        self.input_frame.grid(row=2, column=1)

        self.remember_me_var = tk.IntVar()
        self.remember_me = tk.Checkbutton(self, text="Remember me", variable=self.remember_me_var)
        self.remember_me.grid(row=3, column=1)

        self.button_frame = tk.Frame(self)

        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)

        self.register_button = tk.Button(self.button_frame,
                                      text="Register",
                                      width=15,
                                      font=("Calibri", 12),
                                      command=lambda: self.register())
        self.register_button.grid(row=0, column=1, padx=5)

        self.back_button = tk.Button(self.button_frame,
                                     text="Back",
                                     width=15,
                                     font=("Calibri", 12),
                                     command=lambda: self.router.navigate_back())
        self.back_button.grid(row=0, column=0, padx=5)

        self.button_frame.grid(row=4, column=1, pady=10)

        self.register_result_text = tk.StringVar()
        self.register_result = tk.Label(self, textvariable=self.register_result_text, font=("Calibri", 18))
        self.register_result.grid(row=5, column=1, pady=10)

    def register(self):
        hash = hashlib.sha256(self.password_var.get().encode())
        username = self.login_var.get()
        try:
            result = self.client.send_rpc(RegisterMessage(username, hash.hexdigest()))
        except Exception:
            self.logout()
            return

        if result.code == RegisterResponseCode.EXISTS.value:
            self.register_result_text.set("Account already exists!")
        elif result.code == RegisterResponseCode.SUCCESS.value:
            self.appdata.account = Account(self.login_var.get(), self.password_var.get())
            # saving to config if remember me is checked, deleting config otherwise
            if self.remember_me_var.get() == 1:
                config.save(self.appdata)
            else:
                config.delete()
            self.router.navigate_pop("main/main")