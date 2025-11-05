from pathlib import Path
from datetime import datetime, timezone
import getpass
import json

from mailbox import Mailbox          # your module
from user import User                # your User class: User(email, password)
from message import Message          # your Message class

STORE = "mail_store.json"


def read_store(path=STORE) -> dict:
    p = Path(path)
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def prompt_register():
    print("\n-- Register new account --")
    email = input("Email: ").strip()
    if not email:
        print("Email required.")
        return
    password = getpass.getpass("Password: ").strip()
    if not password:
        print("Password required.")
        return
    user = User(email, password)
    Mailbox.create_mailbox(user, storage_path=STORE)
    print(f"Account created (or already present) for {email}.\n")


def prompt_login():
    print("\n-- Login --")
    email = input("Email: ").strip()
    if not email:
        print("Email required.")
        return None
    password = getpass.getpass("Password: ").strip()
    try:
        mailbox = Mailbox.login(email, password, storage_path=STORE)
        print(f"Logged in as {email}\n")
        return mailbox
    except ValueError as e:
        print("Login failed:", e)
        return None


def show_actions_menu(user_email: str):
    print()
    print(f"Account: {user_email}")
    print("1) List messages")
    print("2) Read message")
    print("3) Send message")
    print("4) Logout")
    print("5) Quit")
    print()


def choose(prompt="> "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        return ""


def list_messages(mailbox: Mailbox):
    mailbox.reload()
    if not mailbox.messages:
        print("No messages.")
        return
    for i, m in enumerate(mailbox.messages, 1):
        # m is your Message instance; assume attributes: header, sender_email, date
        print(f"{i}) {m.header}  from: {m.sender_email}  date: {m.date}")


def read_message(mailbox: Mailbox):
    mailbox.reload()
    if not mailbox.messages:
        print("No messages to read.")
        return
    idx = choose("Message number: ")
    if not idx.isdigit():
        print("Invalid number.")
        return
    i = int(idx) - 1
    if i < 0 or i >= len(mailbox.messages):
        print("Out of range.")
        return
    mailbox.messages[i].display()


def send_message_flow(mailbox: Mailbox):
    store = read_store(STORE)
    to_email = input("To (email): ").strip()
    if not to_email:
        print("Recipient required.")
        return
    if to_email not in store:
        print("Recipient not found in store. Ask them to register first.")
        return
    header = input("Header: ").strip()
    print("Enter body. Finish with a single '.' on its own line.")
    lines = []
    while True:
        try:
            line = input()
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled.")
            return
        if line == ".":
            break
        lines.append(line)
    body = "\n".join(lines)
    # create a minimal user-like object for receiver: only .email required by send_message
    receiver = User(to_email, store[to_email].get("mdp", ""))  # password not used by send_message
    msg = Message("inbox", mailbox.user.email, datetime.now(timezone.utc), header, body)
    try:
        mailbox.send_message(receiver, msg)
        print("Message sent.")
    except Exception as e:
        # ReceiverNotFoundError or other IO errors
        print("Failed to send:", e)


def account_loop(mailbox: Mailbox):
    while True:
        show_actions_menu(mailbox.user.email)
        choice = choose("Select: ")
        if choice == "1":
            list_messages(mailbox)
        elif choice == "2":
            read_message(mailbox)
        elif choice == "3":
            send_message_flow(mailbox)
        elif choice == "4":
            print("Logging out.\n")
            return  # back to top-level login/register
        elif choice == "5" or choice.lower() in ("q", "quit"):
            print("Goodbye.")
            raise SystemExit(0)
        else:
            print("Unknown choice.")


def main():
    print("Simple Mailbox TUI (no dependencies)")
    # ensure store exists
    p = Path(STORE)
    if not p.exists():
        p.write_text(json.dumps({}), encoding="utf-8")

    while True:
        print("\nMain menu:")
        print("1) Login")
        print("2) Register")
        print("3) Quit")
        choice = choose("Select: ")
        if choice == "1":
            mailbox = prompt_login()
            if mailbox:
                try:
                    account_loop(mailbox)
                except SystemExit:
                    return
        elif choice == "2":
            prompt_register()
        elif choice == "3" or choice.lower() in ("q", "quit"):
            print("Bye.")
            return
        else:
            print("Unknown option.")


if __name__ == "__main__":
    main()
