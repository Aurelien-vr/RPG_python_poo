import json
from pathlib import Path
from datetime import datetime, timezone

# minimal custom exception
class ReceiverNotFoundError(Exception):
    pass

class Mailbox:
    """
    Small Mailbox helper:
    - create_mailbox(user, storage_path) : ensure user exists in shared JSON with "mdp"
    - login(email, password, storage_path) -> Mailbox instance (raises ValueError on failure)
    - send_message(receiver_user, message) : store message in receiver's JSON entry
    - reload() : populate self.messages (list of Message instances)
    """

    def __init__(self, user, storage_path: str = "mail_store.json"):
        self.user = user
        self.storage_path = Path(storage_path)
        if not self.storage_path.exists():
            self._save_store({})
        self.messages = []
        self.reload()

    @classmethod
    def create_mailbox(cls, user, storage_path: str = "mail_store.json") -> None:
        """
        Ensure the shared JSON store has an entry for `user` (uses .email and .password).
        Adds 'mdp' if missing (does not overwrite existing non-empty 'mdp').
        """
        path = Path(storage_path)
        if not path.exists():
            path.write_text(json.dumps({}), encoding="utf-8")
        try:
            with path.open("r", encoding="utf-8") as f:
                store = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            store = {}

        entry = store.get(user.email)
        if entry is None:
            store[user.email] = {"mdp": user.password}
            with path.open("w", encoding="utf-8") as f:
                json.dump(store, f, indent=2)
        else:
            if "mdp" not in entry or not entry.get("mdp"):
                entry["mdp"] = user.password
                store[user.email] = entry
                with path.open("w", encoding="utf-8") as f:
                    json.dump(store, f, indent=2)

    @classmethod
    def login(cls, email: str, password: str, storage_path: str = "mail_store.json"):
        """
        Authenticate email/password against the JSON store.
        Returns a Mailbox instance bound to a simple user-like object on success.
        Raises ValueError on failure.
        """
        path = Path(storage_path)
        try:
            with path.open("r", encoding="utf-8") as f:
                store = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            store = {}

        entry = store.get(email)
        if entry is None:
            raise ValueError("User not found")
        mdp = entry.get("mdp", "")
        if mdp != password:
            raise ValueError("Invalid password")

        # Simple user-like object
        user = type("User", (), {})()
        user.email = email
        user.password = password
        return cls(user, storage_path=storage_path)

    def send_message(self, receiver, message) -> None:
        """
        Send a Message instance to `receiver` (an object with .email).
        Raises ReceiverNotFoundError if the receiver is not present in the store.
        Message.date must be a datetime instance (serialized as ISO).
        """
        store = self._load_store()

        if receiver.email not in store:
            raise ReceiverNotFoundError(f"Receiver '{receiver.email}' not found in store.")

        date_iso = message.date.isoformat()
        msg_dict = {
            "box": message.box,
            "sender": message.sender_email,
            "date": date_iso,
            "header": message.header,
            "body": message.body,
        }

        receiver_entry = store[receiver.email]
        numeric_keys = [int(k) for k in receiver_entry.keys() if k.isdigit()]
        next_id = (max(numeric_keys) + 1) if numeric_keys else 1
        receiver_entry[str(next_id)] = msg_dict

        self._save_store(store)

    def reload(self) -> None:
        """
        Load this user's messages from the shared JSON store into self.messages.
        Reconstructs Message objects from stored dicts (requires message.py to exist).
        """
        store = self._load_store()
        entry = store.get(self.user.email, {})
        items = [(k, entry[k]) for k in entry.keys() if k.isdigit()]
        try:
            items.sort(key=lambda kv: int(kv[0]))
        except Exception:
            items.sort(key=lambda kv: kv[0])

        messages = []
        for _id, m in items:
            try:
                date_dt = datetime.fromisoformat(m.get("date"))
            except Exception:
                date_dt = datetime.now(timezone.utc)
            # Import lazily to avoid circular imports in small projects
            from message import Message
            msg_obj = Message(
                m.get("box", ""),
                m.get("sender", ""),
                date_dt,
                m.get("header", ""),
                m.get("body", "")
            )
            messages.append(msg_obj)
        self.messages = messages

    def _load_store(self) -> dict:
        try:
            with self.storage_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_store(self, store: dict) -> None:
        if not self.storage_path.parent.exists():
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with self.storage_path.open("w", encoding="utf-8") as f:
            json.dump(store, f, indent=2)
