#!/usr/bin/env python3
"""Read message screen."""

from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Static, Button

from message import Message


class ReadScreen(Screen):
    """Display a Message instance."""

    def __init__(self, message: Message) -> None:
        super().__init__()
        self.message = message

    def compose(self):
        yield Header(show_clock=False)
        yield Static("Message", id="title")
        yield Static(self.format_message(), id="content")
        yield Horizontal(Button("Back", id="back"), Button("Quit", id="quit"))
        yield Footer()

    def format_message(self) -> str:
        m = self.message
        date_str = m.date.isoformat() if hasattr(m.date, "isoformat") else str(m.date)
        parts = [
            "-" * 40,
            f"From: {m.sender_email}",
            f"Date: {date_str}",
            f"Header: {m.header}",
            "",
            m.body,
            "-" * 40,
        ]
        return "\n".join(parts)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
        else:
            self.app.action_quit()
