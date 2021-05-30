"""Network wordt gebruikt om messages te leveren en om de proposers en acceptors op te slaan.
Ook worden sommige globale variabelen hier opgeslagen, zodat alle computers erbij kunnen."""

from messages import Message

class Network():
    """Network class. Handles the transfer of all messages between computers like a queue;
    first in first out, last in last out."""
    def __init__(self,proposers,acceptors,learners,proposals=0):
        self.proposers = proposers
        self.acceptors = acceptors
        self.learners = learners
        self.proposals = proposals
        self.messagequeue = []

    def update_proposalnum(self,n):
        self.proposals = n

    def find_proposer(self,index):
        return self.proposers[index]

    def find_acceptor(self,index):
        return self.acceptors[index]

    def find_learner(self,index):
        return self.learners[index]

    def queue_message(self,m):
        self.messagequeue.append(m)

    def extract_message(self):
        for i in range(len(self.messagequeue)):
            if self.messagequeue[i].src.failed is False and self.messagequeue[i].dst.failed is False:
                message = self.messagequeue[i]
                self.messagequeue.remove(message)
                return message
        return None
