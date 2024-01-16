import threading
import os


class TimestampGenerator:
    def __init__(self):
        self.lock = threading.Lock()
        self.timestamp = self.load_timestamp_from_file()

    def load_timestamp_from_file(self):
        filename = 'timestamp.txt'
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return int(file.read().strip())
        else:
            self.save_timestamp_to_file(0)
            return 0

    def save_timestamp_to_file(self, timestamp):
        filename = 'timestamp.txt'
        with open(filename, 'w') as file:
            file.write(str(timestamp))

    def get_timestamp(self):
        with self.lock:
            self.timestamp += 1
            print(f"now timestamp is {self.timestamp}")
            self.save_timestamp_to_file(self.timestamp)
            return self.timestamp