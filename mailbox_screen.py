try:
    import pytermgui as ptg
    PTG_AVAILABLE = True
except Exception:
    ptg = None
    PTG_AVAILABLE = False

from datetime import datetime, timezone
from mailbox import Mailbox
from user import User
from message import Message

class MailboxScreen:
    """
    After login: shows message list and actions. Uses pytermgui widgets if available.
    """

    def __init__(self, app, mailbox: Mailbox):
        self.app = app
        self.mailbox = mailbox

    def build_ui(self):
        if not PTG_AVAILABLE:
            return None

        self.mailbox.reload()
        labels = []
        for i, m in enumerate(self.mailbox.messages, start=1):
            labels.append(ptg.Label(f"{i}) {m.header} — from {m.sender_email}"))
        list_box = ptg.ScrollableContainer(*labels, max_height=10) if labels else ptg.Label("(no messages)")

        send_btn = ptg.Button("Send", lambda *_: self._on_send())
        read_btn = ptg.Button("Read", lambda *_: self._on_read())
        logout_btn = ptg.Button("Logout", lambda *_: self.app.logout())

        box = ptg.Box(
            ptg.Label(f"Account: {self.mailbox.user.email}"),
            list_box,
            ptg.Separator(),
            ptg.Container(send_btn, read_btn, logout_btn, align="left"),
            box_sizing=ptg.BoxSizing.STATIC
        )
        return box

    def _on_read(self):
        self.mailbox.reload()
        if not self.mailbox.messages:
            if PTG_AVAILABLE:
                ptg.alert("No messages.")
            else:
                print("No messages.")
            return
        m = self.mailbox.messages[0]
        text = (
            f"From: {m.sender_email}\n"
            f"Header: {m.header}\n"
            f"Date: {m.date}\n\n"
            f"{m.body}"
        )
        if PTG_AVAILABLE:
            ptg.alert(text)
        else:
            print(text)

    def _on_send(self):
        if PTG_AVAILABLE:
            to_email = ptg.ask("To (email): ")
            header = ptg.ask("Header: ")
            body = ptg.ask("Body: ")
        else:
            to_email = input("To (email): ").strip()
            header = input("Header: ").strip()
            body = input("Body: ").strip()

        receiver = User(to_email, "")
        msg = Message("inbox", self.mailbox.user.email, datetime.now(timezone.utc), header, body)
        try:
            self.mailbox.send_message(receiver, msg)
            if PTG_AVAILABLE:
                ptg.alert("Message sent.")
            else:
                print("Message sent.")
        except Exception as e:
            if PTG_AVAILABLE:
                ptg.alert(str(e))
            else:
                print("Failed to send:", e)

    def run_cli(self):
        # CLI loop for mailbox actions
        while True:
            self.mailbox.reload()
            print(f"\nAccount: {self.mailbox.user.email}")
            if not self.mailbox.messages:
                print("(no messages)")
            else:
                for i, m in enumerate(self.mailbox.messages, 1):
                    print(f"{i}) {m.header} — from {m.sender_email} — {m.date}")
            print("\n1) Read first")
            print("2) Send")
            print("3) Logout")
            print("4) Quit")
            choice = input("> ").strip()
            if choice == "1":
                if not self.mailbox.messages:
                    print("No messages.")
                else:
                    self.mailbox.messages[0].display()
            elif choice == "2":
                to = input("To (email): ").strip()
                header = input("Header: ").strip()
                body = input("Body: ").strip()
                receiver = User(to, "")
                msg = Message("inbox", self.mailbox.user.email, datetime.now(timezone.utc), header, body)
                try:
                    self.mailbox.send_message(receiver, msg)
                    print("Sent.")
                except Exception as e:
                    print("Failed to send:", e)
            elif choice == "3":
                self.app.logout()
                return
            else:
                raise SystemExit(0)
