import tkinter as tk
from tkinter import ttk
from manager_client.pages.page import Page
from manager_client.pages.router import Router
from manager_client.network.client import Client
from manager_client.data.appdata import AppData
import manager_client.crypto.crypto as crypto
from manager_network.passwords import Password, GetPasswordsMessage, GetPasswordsResponseMessage, \
    GetPasswordsResponseCode, DeletePasswordMessage, DeleteAllPasswordsMessage


class PasswordsPage(Page):
    def __init__(self, root: tk.Tk, router: Router, client: Client, appdata: AppData):
        Page.__init__(self, root, router, client, appdata)

    def render(self):
        try:
            passwords = self.client.send_rpc(GetPasswordsMessage())
        except Exception:
            self.logout()
            return

        self.grid_columnconfigure((0, 1, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        password_list = []

        if passwords.code == GetPasswordsResponseCode.UNAUTHORIZED.value:
            self.client.logout()
            self.appdata.account = None
            self.router.reset()
        elif passwords.code == GetPasswordsResponseCode.SUCCESS.value:
            password_list = passwords.passwords

        password_list = map(
            lambda e: Password(e.id, e.username, crypto.decrypt(e.password, self.appdata.account.password), e.website),
            password_list)

        self.table = ttk.Treeview(self, column=("id", "username", "website", "password"), displaycolumns=("username", "website", "password"),
                                  show="headings", height=10)

        style = ttk.Style()
        style.configure("TreeView.Heading", font=("Calibri", 18))
        style.configure("Treeview", font=("Calibri", 18), rowheight=50)

        self.table.heading("username", text="Username")
        self.table.heading("website", text="Website")
        self.table.heading("password", text="Password")

        # ButtonRelease because <Button-1> event gets raised before the item is actually selected.
        self.table.bind("<ButtonRelease-1>", lambda e: self.on_selection_changed())

        for password in password_list:
            self.add_password(password)

        self.table.grid(row=0, column=1)

        self.button_frame = tk.Frame(self)

        self.back_button = tk.Button(self.button_frame, text="Back", font=("Calibri", 14), command=lambda: self.router.navigate_back())
        self.back_button.grid(row=0, column=0, padx=15)

        self.delete_all_button = tk.Button(self.button_frame, text="Delete all", font=("Calibri", 14), command=lambda: self.delete_all())
        self.delete_all_button.grid(row=0, column=1, padx=15)

        self.delete_button = tk.Button(self.button_frame, text="Delete", font=("Calibri", 14), command=lambda: self.delete_selected())
        self.delete_button.grid(row=0, column=2)

        self.button_frame.grid(row=1, column=1, pady=15)

    def add_password(self, password: Password):
        self.table.insert('', tk.END, values=(password.id, password.username, password.website, password.password))

    def on_selection_changed(self):
        (id, _, _, _) = self.table.item(self.table.focus())["values"]
        self.selected_id = id

    def delete_selected(self):
        if self.selected_id is not None:
            try:
                self.client.send(DeletePasswordMessage(self.selected_id))
            except Exception:
                self.logout()
                return
            self.selected_id = None
            # requesting re-render to reflect changes
            self.render()

    def delete_all(self):
        try:
            self.client.send(DeleteAllPasswordsMessage())
        except Exception:
            self.logout()
            return
        # requesting re-render to reflect changes
        self.render()