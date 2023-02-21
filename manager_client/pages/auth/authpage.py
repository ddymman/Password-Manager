import tkinter as tk
from PIL import Image, ImageTk
from manager_client.pages.router import Router
from manager_client.pages.page import Page
from manager_client.network.client import Client
from manager_client.data.appdata import AppData


class AuthPage(Page):
    def __init__(self, root: tk.Tk, router: Router, client: Client, appdata: AppData):
        Page.__init__(self, root, router, client, appdata)
        self.img = Image.open("assets/logo.png")
        self.img = ImageTk.PhotoImage(self.img.resize((300, 300)))

        self.button_frame = tk.Frame(self)

    def render(self):
        self.grid_columnconfigure((0, 1, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=0)

        canvas = tk.Canvas(self, width=300, height=300)
        canvas.create_image(0, 0, image=self.img, anchor="nw")
        canvas.grid(row=0, column=1)

        tk.Label(self,
                 text="=---------------------            SIGN UP | LOG IN            ---------------------=",
                 font=("Calibri", 18)
                 ).grid(row=1, column=1, pady=20)

        self.button_frame = tk.Frame(self)

        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        self.button_frame.grid_rowconfigure(0, weight=1)

        tk.Button(self.button_frame,
                  text="Login",
                  font=("Calibri", 14),
                  command=lambda: self.router.navigate_to("auth/login"),
                  width=15
                  ).grid(row=0, column=0, padx=15)

        tk.Button(self.button_frame,
                  text="Register",
                  font=("Calibri", 14),
                  command=lambda: self.router.navigate_to("auth/register"),
                  width=15
                  ).grid(row=0, column=1, padx=15)

        self.button_frame.grid(row=2, column=1)
