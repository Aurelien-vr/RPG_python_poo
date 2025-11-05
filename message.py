class Message:
    def __init__(self, sender_email: str, header: str, body: str, box: str, date:str):
        self.sender_email = sender_email
        self.header = header
        self.body = body
        self.box = box
        self.date = date

    def __repr__(self):
        return f"Message(from='{self.sender_email}', header='{self.header}', box='{self.box}',  date='{self.date}')"

    def display(self):
        print(f"From: {self.sender_email}")
        print(f"Header: {self.header}")
        print(f"Box: {self.box}")
        print(f"Box: {self.date}")
        print("Body:")
        print(self.body)