#!/usr/bin/env python3
"""
Top-level Textual App configuration.

This file wires the screens together and provides the entry SCREENS mapping.
"""
from __future__ import annotations
from pathlib import Path

from textual.app import App

from screens.main_menu import MainMenu
from screens.login_screen import LoginScreen
from screens.mailbox_screen import MailboxScreen
from screens.compose_screen import ComposeScreen

STORE = "mail_store.json"


class MailboxApp(App):
    """The Textual App. SCREENS must map names to Screen classes (not instances)."""

    SCREENS = {
        "main": MainMenu,
        "login": LoginScreen,
        "mailbox": MailboxScreen,
        "compose": ComposeScreen,
    }

    mailbox = None  # set to Mailbox instance after login

    def on_mount(self) -> None:
        # ensure store file exists
        p = Path(STORE)
        if not p.exists():
            p.write_text("{}", encoding="utf-8")
        # push initial screen by name; Textual will instantiate the class
        self.push_screen("main")

    def action_quit(self) -> None:
        self.exit()
