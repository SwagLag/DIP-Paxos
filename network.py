from messages import Message

class Network():
    """Network class. Handles the transfer of all messages between computers like a queue;
    first in first out, last in last out."""
    def __init__(self):
        self.messagequeue = []

