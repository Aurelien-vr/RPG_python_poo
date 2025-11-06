#!/usr/bin/env python3
"""Login screen."""

from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Static, Input, Button

from mailbox import Mailbox  # your existing mailbox module
STORE = "mail_store.json"


class LoginScreen(Screen):
    """Prompt user for email and password, then set app.mailbox on success."""

    def compose(self):
        yield Header(show_clock=False)
        yield Static("Login", id="title")
        yield Input(placeholder="Email", id="email")
        yield Input(placeholder="Password", password=True, id="password")
        yield Horizontal(Button("Submit", id="submit"), Button("Back", id="back"))
        yield Static("", id="status")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id
        status = self.query_one("#status", Static)
        if bid == "submit":
            email = self.query_one("#email", Input).value.strip()
            password = self.query_one("#password", Input).value.strip()
            if not email or not password:
                status.update("Email and password required.")
                return
            try:
                mailbox = Mailbox.login(email, password, storage_path=STORE)
            except ValueError as e:
                status.update(f"Login failed: {e}")
                return
            self.app.mailbox = mailbox
            self.app.push_screen("mailbox")
        elif bid == "back":
            self.app.pop_screen()
