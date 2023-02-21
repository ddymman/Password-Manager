# from network.client import Client

# client = Client()
# client.connect("127.0.0.1")

# client.sock.send('amogus'.encode())

import tkinter as tk
import json
from manager_client.pages.router import Router
from manager_client.pages.auth.authpage import AuthPage
from manager_client.pages.auth.loginpage import LoginPage
from manager_client.pages.auth.registerpage import RegisterPage

from manager_client.pages.main.mainpage import MainPage
from manager_client.pages.main.passwords import PasswordsPage
from manager_client.pages.main.addpassword import AddPasswordPage
from manager_client.pages.main.settings import SettingsPage

from manager_network.login import LoginMessage, LoginResponseCode, LoginResponseMessage
from manager_client.network.client import Client
from manager_client.data.appdata import AppData
import manager_client.utils.config as config
import manager_client.crypto.crypto as crypto

# todo: load from config
appdata = config.load()
if appdata is None:
    appdata = AppData()


# Creating a client and connecting to a localhost server
client = Client()
client.connect("127.0.0.1")

# trying to authenticate with saved account
if appdata.account is not None:
    response = client.send_rpc(LoginMessage(appdata.account.username, crypto.hash_pass(appdata.account.password)))

    if response.code != LoginResponseCode.SUCCESS.value:
        appdata.account = None

# Creating a simple tkinter window
window = tk.Tk()
window.geometry("800x600")
window.minsize(800, 600)

#window.resizable(False, False)
#window.configure(bg="blue")

# Creating a router for easy page-switching
router = Router()
routes = {
    "auth/main": AuthPage(window, router, client, appdata),
    "auth/login": LoginPage(window, router, client, appdata),
    "auth/register": RegisterPage(window, router, client, appdata),
    "main/main": MainPage(window, router, client, appdata),
    "main/passwords": PasswordsPage(window, router, client, appdata),
    "main/add_password": AddPasswordPage(window, router, client, appdata),
    "main/settings": SettingsPage(window, router, client, appdata)
}

router.set_routes(routes, "auth/main")

# if authentication was successful, switch to main page
if appdata.account is not None:
    router.navigate_pop("main/main")

# Starting the window
window.mainloop()