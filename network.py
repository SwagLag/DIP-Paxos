from queue import Queue
from messages import Message

class Network():
    """Network class. Handles the transfer of all messages between computers like a queue;
    first in first out, last in last out."""
    def __init__(self):
        self.messagequeue = []

    def Queue_Message(self,message: Message):
        self.messagequeue.append(message)

    def Extract_Message(self):
        for m in self.messagequeue:
            if m.src.failed == False and m.dst.failed == False:
                return m
        return None