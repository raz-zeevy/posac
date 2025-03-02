import os.path

from lib.utils import SESSIONS_HISTORY

MAX_LENGTH = 100

class SessionsHistory:
    def __init__(self, callback : callable = None):
        self.history = []
        self.file_path = SESSIONS_HISTORY
        self.callback = callback
        self.load_history()

    def load_history(self):
        if os.path.exists(self.file_path):
            self.read_from_file()

    # Read and Write
    def write_to_file(self):
        with open(SESSIONS_HISTORY, 'w', encoding='utf-8') as file:
            file.write("\n".join(self.history[-1*MAX_LENGTH:]))

    def read_from_file(self):
        try:
            with open(SESSIONS_HISTORY, 'r', encoding='utf-8') as file:
                content = file.read()
                if content:
                    self.history = content.split("\n")
        except FileNotFoundError:
            self.history = []

    # Setters
    def add(self, path):
        self.history.append(path)
        self.write_to_file()
        if hasattr(self, 'callback') and self.callback:
            self.callback()

    def clear(self):
        self.history = []
        self.write_to_file()
        if hasattr(self, 'callback') and self.callback:
            self.callback()

    # Getters
    def get_n(self, n):
        rec_set = set()
        for rec in self.history[::-1]:
            if len(rec_set) == n:
                break
            if rec not in rec_set:
                rec_set.add(rec)
        return list(rec_set)

    def get_all(self):
        return self.history


