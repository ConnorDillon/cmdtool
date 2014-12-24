import sys


class TestLog:
    def __init__(self):
        self.data = []

    def write(self, s):
        self.data.append(s)

    def flush(self):
        pass

    def __enter__(self):
        sys.stderr = self
        return self.data

    def __exit__(self, *_):
        sys.stdout = sys.__stderr__

