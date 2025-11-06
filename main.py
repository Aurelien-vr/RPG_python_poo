
#!/usr/bin/env python3
"""Entry point for the Textual Mailbox TUI."""
from mailbox_app import MailboxApp


def main() -> None:
    app = MailboxApp()
    app.run()


if __name__ == "__main__":
    main()
