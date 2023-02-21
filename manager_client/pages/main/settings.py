import tkinter as tk
from manager_client.pages.page import Page
from manager_client.pages.router import Router
from manager_client.network.client import Client
from manager_client.data.appdata import AppData
from manager_network.passwords import DeleteAllPasswordsMessage

class SettingsPage(Page):
    def __init__(self, root: tk.Tk, router: Router, client: Client, appdata: AppData):
        Page.__init__(self, root, router, client, appdata)

    def render(self):
        self.grid_columnconfigure((0, 1, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.clear_all_data_button = tk.Button(self, text="clear all data", font=("Calibri", 18), width=30, command=lambda: self.clear_all_data())
        self.clear_all_data_button.grid(row=0, column=1, pady=60)

        self.logout_button = tk.Button(self, text="logout", font=("Calibri", 18), width=30, command=lambda: self.logout())
        self.logout_button.grid(row=1, column=1, pady=60)

        self.back_button = tk.Button(self, text="back", font=("Calibri", 18), width=30, command=lambda: self.router.navigate_back())
        self.back_button.grid(row=2, column=1, pady=60)

    def clear_all_data(self):
        try:
            self.client.send(DeleteAllPasswordsMessage())
        except Exception:
            self.logout()
