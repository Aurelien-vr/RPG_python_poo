from datetime import datetime

class Message:
    def __init__(self, box: str, sender_email: str, date: datetime, header: str, body: str):
        self.box = box
        self.sender_email = sender_email
        self.date = date
        self.header = header
        self.body = body

    def __repr__(self):
        return f"Message(from='{self.sender_email}', header='{self.header}', box='{self.box}', date='{self.date}')"

    def display(self):
        print("-" * 40)
        print(f"From:   {self.sender_email}")
        print(f"Header: {self.header}")
        print(f"Box:    {self.box}")
        print(f"Date:   {self.date}")
        print("Body:")
        print(self.body)
        print("-" * 40)
