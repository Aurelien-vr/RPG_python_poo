class User:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User(email={self.email!r})"
