import tkinter as tk
from PIL import Image, ImageTk
from manager_client.pages.page import Page
from manager_client.pages.router import Router
from manager_client.network.client import Client
from manager_client.data.appdata import AppData
import manager_client.crypto.crypto as crypto
import random
import string
from manager_network.passwords import AddPasswordMessage, Password, AddPasswordResponseCode


class AddPasswordPage(Page):
    def __init__(self, root: tk.Tk, router: Router, client: Client, appdata: AppData):
        Page.__init__(self, root, router, client, appdata)

        self.img = Image.open("assets/logo.png")
        self.img = ImageTk.PhotoImage(self.img.resize((300, 300)))

    def render(self):
        self.grid_columnconfigure((0, 1, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)

        canvas = tk.Canvas(self, width=300, height=300)
        canvas.create_image(0, 0, image=self.img, anchor="nw")
        canvas.grid(row=0, column=1)

        self.input_frame = tk.Frame(self)
        self.input_frame.grid_columnconfigure((0, 1), weight=1)
        self.input_frame.grid_rowconfigure((0, 1, 2), weight=1)

        tk.Label(self.input_frame, text="Username: ", font=("Calibri", 14), justify="center").grid(row=0, column=0, padx=40, pady=5)

        self.username_input_var = tk.StringVar()
        self.username_input = tk.Entry(self.input_frame,
                                       textvariable=self.username_input_var,
                                       width=50,
                                       font=("Calibri", 14)
                                       )
        self.username_input.grid(row=0, column=1)

        tk.Label(self.input_frame, text="Website: ", font=("Calibri", 14), justify="center").grid(row=1, column=0, padx=40, pady=5)

        self.website_input_var = tk.StringVar()
        self.website_input = tk.Entry(self.input_frame,
                                      textvariable=self.website_input_var,
                                      width=50,
                                      justify="left",
                                      font=("Calibri", 14))
        self.website_input.grid(row=1, column=1, sticky="w")

        tk.Label(self.input_frame, text="Password: ", font=("Calibri", 14), justify="center").grid(row=2, column=0, padx=40, pady=5)

        self.password_frame = tk.Frame(self.input_frame)
        self.password_frame.grid_columnconfigure((0, 1), weight=0)
        self.password_frame.grid_rowconfigure(0, weight=0)

        self.password_input_var = tk.StringVar()
        self.password_input = tk.Entry(self.password_frame,
                                       textvariable=self.password_input_var,
                                       width=40,
                                       font=("Calibri", 14)
                                       )
        self.password_input.grid(row=0, column=0)


        self.generate_button = tk.Button(self.password_frame,
                                         text="Generate",
                                         width=11,
                                         font=("Calibri", 10),
                                         command=lambda: self.generate())
        self.generate_button.grid(row=0, column=1, padx=8, sticky="w")

        self.password_frame.grid(row=2, column=1)

        tk.Button(self.input_frame, text="Cancel", font=("Calibri", 10), justify="center", width=20, command=lambda: self.router.navigate_back()).grid(row=3, column=0, padx=40, pady=5)
        tk.Button(self.input_frame, text="Add", font=("Calibri", 10), justify="center", width=70, command=lambda: self.add()).grid(row=3, column=1, sticky="w")

        self.input_frame.grid(row=2, column=1)

        self.result_text_var = tk.StringVar()
        self.result_text = tk.Label(self, textvariable=self.result_text_var, font=("Calibri", 18))
        self.result_text.grid(row=3, column=1)

        pass

    def generate(self):
        password = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        self.password_input_var.set(password)

    def add(self):
        encrypted = crypto.encrypt(self.password_input_var.get(), self.appdata.account.password)
        password = Password(0, self.username_input_var.get(), encrypted, self.website_input_var.get())

        try:
            resp = self.client.send_rpc(AddPasswordMessage(password))
        except Exception:
            self.logout()
            return

        if resp.code == AddPasswordResponseCode.UNAUTHORIZED.value:
            self.client.logout()
            self.appdata.account = None
            self.router.reset()
        elif resp.code == AddPasswordResponseCode.SUCCESS.value:
            self.router.navigate_back()
