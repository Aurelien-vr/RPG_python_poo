try:
    import pytermgui as ptg
    PTG_AVAILABLE = True
except Exception:
    ptg = None
    PTG_AVAILABLE = False

from mailbox import Mailbox
from user import User

STORE = "mail_store.json"

class LoginScreen:
    """
    Login screen using pytermgui (if available) or fallback CLI.
    - On successful login calls app.on_login(mailbox)
    - On register, creates a mailbox entry using Mailbox.create_mailbox(user)
    """

    def __init__(self, app):
        self.app = app
        self.email_field = None
        self.password_field = None

    def build_ui(self):
        if not PTG_AVAILABLE:
            return None

        # Very small pytermgui UI
        self.email_field = ptg.InputField(title="Email")
        self.password_field = ptg.InputField(title="Password", password=True)
        login_btn = ptg.Button("Login", lambda *_: self._on_login_clicked())
        register_btn = ptg.Button("Register", lambda *_: self._on_register_clicked())
        box = ptg.Box(
            ptg.Label("Login"),
            self.email_field,
            self.password_field,
            ptg.Separator(),
            ptg.Container(login_btn, register_btn, align="left"),
            box_sizing=ptg.BoxSizing.STATIC
        )
        return box

    def _on_login_clicked(self):
        email = self.email_field.value.strip()
        password = self.password_field.value.strip()
        try:
            mb = Mailbox.login(email, password, storage_path=STORE)
        except ValueError as e:
            if PTG_AVAILABLE:
                ptg.alert(str(e))
            else:
                print("Login failed:", e)
            return
        self.app.on_login(mb)

    def _on_register_clicked(self):
        email = self.email_field.value.strip()
        password = self.password_field.value.strip()
        if not email or not password:
            if PTG_AVAILABLE:
                ptg.alert("Email and password required.")
            else:
                print("Email and password required.")
            return
        user = User(email, password)
        Mailbox.create_mailbox(user, storage_path=STORE)
        if PTG_AVAILABLE:
            ptg.alert("Account created (or already exists).")
        else:
            print("Account created (or already exists).")

    def run_cli(self):
        # fallback CLI login/register
        while True:
            print("\nLogin or register")
            print("1) Login")
            print("2) Register")
            print("3) Quit")
            choice = input("> ").strip()
            if choice == "1":
                email = input("Email: ").strip()
                password = input("Password: ").strip()
                try:
                    mb = Mailbox.login(email, password, storage_path=STORE)
                except ValueError as e:
                    print("Login failed:", e)
                    continue
                self.app.on_login(mb)
                return
            elif choice == "2":
                email = input("Email: ").strip()
                password = input("Password: ").strip()
                user = User(email, password)
                Mailbox.create_mailbox(user, storage_path=STORE)
                print("Account created.")
            else:
                raise SystemExit(0)
