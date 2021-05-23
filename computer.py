class Computer():
    """Computer to be used in the Paxos Simulation. A computer is either a proposer or an acceptor, albeit
    this is not specifically defined in the algorithm."""
    def __init__(self, id: int, networkaccess, ):
        self.id = id
        self.failed = False  # Een computer die gefaald is, doet niks. Kan wel weer gerepareerd worden.
        self.messagehistory = []  # Sla alles op; handig voor debuggen
        self.propid = 0 # Id of the previous proposer. Determines whether the computer accepets a proposal or not.
        self.value = None





