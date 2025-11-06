#!/usr/bin/env python3
"""Compose screen (single-line body for simplicity)."""

from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json

from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Static, Input, Button

from user import User
from message import Message

STORE = "mail_store.json"


class ComposeScreen(Screen):
    """Compose a message and send it via the Mailbox backend."""

    def compose(self):
        yield Header(show_clock=False)
        yield Static("Compose", id="title")
        yield Input(placeholder="To (email)", id="to")
        yield Input(placeholder="Header", id="header")
        yield Input(placeholder="Body (single line)", id="body")
        yield Horizontal(Button("Send", id="send"), Button("Back", id="back"))
        yield Static("", id="status")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id
        status = self.query_one("#status", Static)
        if bid == "send":
            to_email = self.query_one("#to", Input).value.strip()
            header = self.query_one("#header", Input).value.strip()
            body = self.query_one("#body", Input).value.strip()
            if not to_email:
                status.update("Recipient required.")
                return
            # quick check in the store file
            try:
                p = Path(STORE)
                if p.exists():
                    store = json.loads(p.read_text(encoding="utf-8"))
                else:
                    store = {}
            except Exception as e:
                status.update(f"Failed to read store: {e}")
                return
            if to_email not in store:
                status.update("Recipient not found. Ask them to register first.")
                return
            receiver = User(to_email, store[to_email].get("mdp", ""))
            msg = Message("inbox", self.app.mailbox.user.email, datetime.now(timezone.utc), header, body)
            try:
                self.app.mailbox.send_message(receiver, msg)
                status.update("Message sent.")
                # Refresh mailbox screen only when the user sends a message.
                try:
                    screen = self.app.get_screen("mailbox")
                except Exception:
                    screen = None
                if screen and hasattr(screen, "load_messages"):
                    try:
                        screen.load_messages()
                    except Exception:
                        pass
            except Exception as e:
                status.update(f"Failed to send: {e}")
        elif bid == "back":
            self.app.pop_screen()
