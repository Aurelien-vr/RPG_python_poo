#!/usr/bin/env python3
"""Main menu screen."""

from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer, Static, Button

from utils.banner import banner_text


class MainMenu(Screen):
    """Main menu with simple Login/Quit buttons."""

    def compose(self):
        yield Header(show_clock=False)
        yield Static(banner_text("Mailbox"), id="banner", expand=False)
        yield Container(
            Static("Choose:", id="intro"),
            Horizontal(
                Button("Login", id="login"),
                Button("Quit", id="quit"),
                id="main_buttons",
            ),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "login":
            self.app.push_screen("login")
        elif event.button.id == "quit":
            self.app.action_quit()
