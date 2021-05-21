class Computer():
    """Computer to be used in the Paxos Simulation. A computer is either a proposer or an acceptor, albeit
    this is not specifically defined in the algorithm."""
    def __init__(self, id):
        self.id = id
        self.failed = False  # Een computer die gefaald is, doet niks, maar kan wel weer gerepareerd worden.

    def Deliver_Message(self, c, m):

