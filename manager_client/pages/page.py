import tkinter as tk
from abc import abstractmethod

from manager_client.pages.route import Route
from manager_client.pages.router import Router
from manager_client.network.client import Client
from manager_client.data.appdata import AppData

# Simple page implementing basic route, tk.Frame, and re-rendering when shown
class Page(Route, tk.Frame):
    def __init__(self, root: tk.Tk, router: Router, client: Client, appdata: AppData):
        tk.Frame.__init__(self, root)
        self.router = router
        self.client = client
        self.appdata = appdata

    @abstractmethod
    def render(self): None

    def show(self):
        self.render()
        self.pack(fill='both', expand=True)

    def hide(self):
        self.pack_forget()

    def logout(self):
        self.client.logout()
        self.appdata.account = None
        self.router.reset()

