#!/usr/bin/env python3
"""Mailbox inbox screen: list, refresh, read, compose, logout."""

from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json

from textual.screen import Screen
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Static, DataTable, Label, Button

from user import User
from message import Message
from mailbox import Mailbox
from utils.banner import banner_text

STORE = "mail_store.json"


class MailboxScreen(Screen):
    """Inbox view with a DataTable of messages."""

    def compose(self):
        yield Header(show_clock=False)
        yield Static(banner_text("Inbox", width=60), id="inbox_banner", expand=False)
        yield Label("", id="account")
        yield DataTable(id="table")
        yield Horizontal(
            Button("Refresh", id="refresh"),
            Button("Read", id="read"),
            Button("Compose", id="compose"),
            Button("Logout", id="logout"),
            Button("Quit", id="quit"),
        )
        yield Static("", id="status")
        yield Footer()

    def on_mount(self) -> None:
        # prepare table on mount
        self.load_messages()

    def load_messages(self) -> None:
        """Reload mailbox messages and populate the DataTable.

        This method is defensive about DataTable.clear API differences across
        Textual versions.
        """
        mailbox: Mailbox | None = getattr(self.app, "mailbox", None)
        status = self.query_one("#status", Static)
        table = self.query_one(DataTable)

        # Clear the table in a way compatible with multiple textual versions.
        try:
            table.clear()
        except TypeError:
            # fallback: remove and recreate the DataTable widget
            parent = table.parent
            table.remove()
            table = DataTable(id="table")
            parent.mount(table)

        # (re)define columns
        table.add_columns("No", "From", "Date", "Header")

        if mailbox is None:
            status.update("No mailbox loaded.")
            return

        mailbox.reload()
        for i, m in enumerate(mailbox.messages, start=1):
            date_str = m.date.isoformat() if hasattr(m.date, "isoformat") else str(m.date)
            table.add_row(str(i), m.sender_email, date_str, m.header)

        self.query_one("#account", Label).update(f"Account: {mailbox.user.email}")
        status.update(f"{len(mailbox.messages)} message(s)")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id
        if bid == "refresh":
            self.load_messages()
        elif bid == "read":
            table = self.query_one(DataTable)
            if table.row_count == 0:
                self.query_one("#status", Static).update("No messages to read.")
                return
            if table.cursor_row is None:
                self.query_one("#status", Static).update("Select a row first (use arrows).")
                return
            row = table.get_row_at(table.cursor_row)
            idx = int(row[0]) - 1
            mailbox: Mailbox = self.app.mailbox
            msg = mailbox.messages[idx]
            # ReadScreen takes a Message instance — push an instance
            from .read_screen import ReadScreen
            self.app.push_screen(ReadScreen(msg))
        elif bid == "compose":
            self.app.push_screen("compose")
        elif bid == "logout":
            self.app.mailbox = None
            self.app.pop_screen()
        elif bid == "quit":
            self.app.action_quit()
