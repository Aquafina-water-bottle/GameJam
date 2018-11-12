import time

class Timer:
    def __init__(self):
        self.beginning_time = 0
        self.time_length = 0

    def start(self, time_length):
        self.beginning_time = time.time()
        self.time_length = time_length

    def get(self):
        """
        decrements from time_length to 0
        """
        current_time = time.time()
        time_difference = self.time_length - (current_time - self.beginning_time)
        return time_difference

    @property
    def ended(self):
        return self.get() <= 0

class Ticker:
    """
    literally just stores a unique tick lmao
    """
    def __init__(self):
        self._tick = 0

    def update(self):
        self._tick += 1

    @property
    def tick(self):
        return self._tick






