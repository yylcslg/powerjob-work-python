from queue import Queue


class InstanceLogQueue:

    def __init__(self, maxsize = 1000000):
        self.q = Queue(maxsize=maxsize)

    @property
    def queue(self):
        return self.q


logQueue = InstanceLogQueue(maxsize = 1000000)
