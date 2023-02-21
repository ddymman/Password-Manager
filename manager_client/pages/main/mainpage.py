import tkinter as tk
from manager_client.pages.page import Page
from manager_client.pages.router import Router
from manager_client.network.client import Client
from manager_client.data.appdata import AppData


class MainPage(Page):
    def __init__(self, root: tk.Tk, router: Router, client: Client, appdata: AppData):
        Page.__init__(self, root, router, client, appdata)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)

    def render(self):
        username = self.appdata.account.username if self.appdata.account is not None else ""

        tk.Label(self,
                 text=f"Welcome, {username}.\nWhat would you like to do?",
                 font=("Calibri", 18),
                 justify="left",
                 anchor="w",
                 ).grid(row=0, column=0, padx=35, pady=25, sticky="w")

        tk.Button(self,
                  text="My passwords",
                  font=("Calibri", 14),
                  command=lambda: self.router.navigate_to("main/passwords"),
                  width=20
                  ).grid(row=1, column=0, padx=35, pady=50, sticky="w")

        tk.Button(self,
                  text="Add password",
                  font=("Calibri", 14),
                  command=lambda: self.router.navigate_to("main/add_password"),
                  width=20
                  ).grid(row=2, column=0, padx=35, pady=50, sticky="w")

        tk.Button(self,
                  text="Settings",
                  font=("Calibri", 14),
                  command=lambda: self.router.navigate_to("main/settings"),
                  width=20
                  ).grid(row=3, column=0, padx=35, pady=50, sticky="w")
