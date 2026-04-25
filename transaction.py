class Transaction(object):
    def __init__(self, sender: str, receiver: str, data: str):
        self.sender = sender
        self.receiver = receiver
        self.data = data
    
    def to_string(self) -> str:
        return f"{self.sender}{self.receiver}{self.data}"
    
    def sign(self, private_key):
        pass

    def is_valid(self) -> bool:
        pass
