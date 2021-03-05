# 2021-1-25
from datetime import datetime, timezone

class Engine():
    def __init__(self, name, ID=0):
        self.name = name
        self.text = None
        self.time = None
        self.ID = ID
    def input_text(self, text=""):
        self.text = text
        self.time_stamp()
    def time_stamp(self):
        self.time = datetime.now(timezone.utc)
    def display(self):
        print(f"{self.name} [{self.time.astimezone().strftime('%Y-%m-%d %H:%M:%S')}]: {self.text}")
