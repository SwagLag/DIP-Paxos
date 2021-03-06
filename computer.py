# class Computer():
#     """Computer to be used in the Paxos Simulation. A computer is either a proposer or an acceptor, albeit
#     this is not specifically defined in the algorithm."""
#     def __init__(self, id: int, type:str, networkaccess):
#         if type.upper() == "PROPOSER":
#             self.id = "{}{}".format("P",id)
#         elif type.upper() == "ACCEPTOR":
#             self.id = "{}{}".format("A", id)
#         elif type.upper() == "LEARNER":
#             self.id = "{}{}".format("L", id)
#         self.type = type
#         self.failed = False  # Een computer die gefaald is, doet niks. Kan wel weer gerepareerd worden.
#         self.messagehistory = []  # Sla alles op; handig voor debuggen
#         self.state = 0  # Finite State method of handling messages.
#         self.propid = -1  # Id of the previous proposer. Determines whether the computer accepets a proposal or not.
#         self.value = None  # Value given by the proposer during the accept stage.
#
#     def process_message(self, m: Message):
#         """Processes a given message."""
#         if self.type ==

import numpy as np
from messages import Message

class BaseComputer():
    """Defines some methods that all other computer classes should have."""
    def __init__(self,id):
        self.id = id
        self.failed = False

    def process_message(self,m):
        pass

class Proposer(BaseComputer):
    def __init__(self,id,n_A,n_L):
        super().__init__(id)
        self.acceptors = n_A
        self.learners = n_L

        self.network = None  # Define this in the simulation code later on, or else it will throw errors!!
        self.previousproposals = 0  # Amount of proposals that have been done previously.

        self.proposalid = -1  # Proposal id.
        self.processed = 0  # Processed message. Used as a trigger for when n_A == processed to continue with logics.
        self.promised = 0  # Acceptors that promised to the proposer
        self.accepted = 0  # Acceptors that accepted the proposer

        self.historyproposed = []  # Contains previous initially proposed values.
        self.historyaccepted = []  # Contains previous accepted values.
        self.historyreached = []  # Contains information on whether consensus was reached.

        self.state = 0
        # STATES:
        # 0: Idle
        # 1: Pending Proposal
        # 2: Pending Accept
        # 3: Success (Consensus bereikt)
        self.proposed = None  # Value that was initially proposed externally.
        self.value = None  # Value that the proposer is trying to get consensus on.

        self.consensus = False  # Het uiteindelijke doel; proberen consensus te krijgen!

    def increment_proposal(self):
        # Step 1: Get the amount of previous proposals from the network.
        self.previousproposals = self.network.proposals
        # Step 2: Get proposal id, which is the amount of previous proposals plus one.
        self.proposalid = self.previousproposals + 1
        # Step 3: Tell network that a new proposal is occuring.
        self.network.update_proposalnum(self.proposalid)

    def process_message(self,m):
        if self.state in [1,2]:  # Alleen als het nodig is tellen we berichten om te kijken of we een consensus bereiken.
            self.processed += 1  # Anders gebeuren er 'grappige' dingen; bijv. de proposer gaat dan in bepaalde intervals
                                 # meteen al kijken of ie consensus heeft (en faalt dus direct)
        if self.state == 1:  # Prepare stage
            if m.type == "PROMISE":
                self.promised += 1
                if m.value is not None and m.src.state == 1:
                    self.value = m.value
                if self.processed == self.acceptors:
                    if self.promised / self.processed >= 0.5:  # Consensus reached.
                        for i in range(self.acceptors):
                            self.network.queue_message(Message(self, self.network.find_acceptor(i), "ACCEPT", self.value))
                        self.state = 2
                    else:  # Failure, try again with a higher proposerid.
                        self.state = 1
                        self.increment_proposal()
                        for i in range(self.acceptors):
                            self.network.queue_message(Message(self, self.network.find_acceptor(i), "PREPARE", self.value))
                    # Reset values
                    self.processed, self.promised = 0,0

            elif m.type == "REJECTED":
                if self.processed == self.acceptors:
                    if self.promised / self.processed >= 0.5:  # Consensus reached.
                        self.state = 2
                        for i in range(self.acceptors):
                            self.network.queue_message(Message(self, self.network.find_acceptor(i), "ACCEPT", self.value))
                    else:
                        self.state = 1
                        self.increment_proposal()
                        for i in range(self.acceptors):
                            self.network.queue_message(Message(self, self.network.find_acceptor(i), "PREPARE", self.value))
                    # Reset values
                    self.processed, self.promised = 0, 0

        elif self.state == 2:  # Acceptance stage
            if m.type == "ACCEPTED":
                m.src.state = 0  # Set the acceptor's state to 0.
                self.accepted += 1
                if self.processed == self.acceptors:
                    if self.accepted / self.processed >= 0.5:  # Consensus reached.
                        self.state = 3
                        self.consensus = True
                        for i in range(self.learners):
                            self.network.queue_message(Message(self, self.network.find_learner(i), "SUCCESS", self.value))
                        # Proposer is dan klaar; schrijf log gegevens in.
                        self.historyproposed.append(self.proposed)
                        self.historyaccepted.append(self.value)
                        self.historyreached.append(self.consensus)
                    else:
                        self.state = 1
                        self.increment_proposal()
                        for i in range(self.acceptors):
                            self.network.queue_message(Message(self, self.network.find_acceptor(i), "PREPARE", self.value))
                    self.processed, self.accepted = 0, 0

            elif m.type == "REJECTED":
                if self.processed == self.acceptors:
                    if self.accepted / self.processed >= 0.5:  # Consensus reached.
                        self.state = 3
                        self.consensus = True
                        for i in range(self.learners):
                            self.network.queue_message(Message(self, self.network.find_learner(i), "SUCCESS", self.value))
                        # Proposer is dan klaar; schrijf log gegevens in.
                        self.historyproposed.append(self.proposed)
                        self.historyaccepted.append(self.value)
                        self.historyreached.append(self.consensus)
                    else:
                        self.state = 1
                        self.increment_proposal()
                        for i in range(self.acceptors):
                            self.network.queue_message(Message(self, self.network.find_acceptor(i), "PREPARE", self.value))
                    self.processed, self.accepted = 0, 0

    def handle_external_message(self,m):
        # Logging
        if self.proposed is not None and self.value is not None and self.consensus is False:
            self.historyproposed.append(self.proposed)
            self.historyaccepted.append(self.value)
            self.historyreached.append(self.consensus)
        # End of logging.
        self.state = 1
        self.consensus = False
        self.increment_proposal()
        # Bericht zou altijd een PROPOSAL bericht moeten zijn.
        # Source is ook altijd None.
        # (deze methode wordt ook alleen gebruikt bij het handelen van events)
        self.proposed = m.value
        self.value = m.value
        # Verstuur PREPARE naar alle acceptors.
        for i in range(self.acceptors):
            self.network.queue_message(Message(self,self.network.find_acceptor(i),"PREPARE",self.value))


class Acceptor(BaseComputer):
    def __init__(self,id):
        super().__init__(id)
        self.network = None  # Define this in the simulation code later on, or else it will throw errors!!

        self.propid = None  # Id of the previous proposer, is copied from a proposer in a message when necessary.
        self.prevpropid = None

        self.state = 0
        # STATES:
        # 0: Initial state. Does not pass over values after receiving a PROMISE for the first time.
        # 1: Correcting state. Passes over it's stored value after receiving a PROMISE message.
        # If ACCEPTOR receives a ACCEPT message, it's state is set to 1.
        # If ACCEPTOR sends a ACCEPTED message, it returns to state 0.
        self.value = None  # Value from a message.

    def process_message(self,m):
        if m.type == "PREPARE":  # Neem alleen het ID over als het hoger is dan het huidige ID.
            if self.propid is not None:
                if self.propid < m.src.proposalid:
                    # Dit is een soort lock; ID's die eronder zitten mogen hier niks
                    self.prevpropid = self.propid  # Sla vorige id op om te printen in de simulatie.
                    self.propid = m.src.proposalid
                    self.network.queue_message(Message(self,m.src,"PROMISE",self.value))
                else:  # Failure, proposalid of message lower than registered proposalid.
                    self.network.queue_message(Message(self,m.src,"REJECTED",None))
            else:
                self.propid = m.src.proposalid
                self.network.queue_message(Message(self, m.src, "PROMISE", self.value))

        elif m.type == "ACCEPT":
            if self.propid <= m.src.proposalid:
                self.value = m.value
                self.state = 1
                self.network.queue_message(Message(self,m.src,"ACCEPTED",self.value))
            else:
                self.network.queue_message(Message(self,m.src,"REJECTED",None))

class Learner(BaseComputer):
    def __init__(self,id):
        super().__init__(id)
        self.network = None  # Define this in the simulation code later on, or else it will throw errors!!
        self.alphabetkey = "abcdefghijklmnopqrstuvwxyz ,"
        self.nlmatrice = np.full((len(self.alphabetkey),len(self.alphabetkey)),0)
        self.enmatrice = np.full((len(self.alphabetkey),len(self.alphabetkey)),0)
        self.total = 0  # Total amount of adjustments done to translation matrices

    def process_message(self,m):
        if m.type == "SUCCESS":  # Safety check.
            request,value = m.value.split(":")
            if len(value) == 1:  # Vanwege irritante python formatting is een input met ????n letter eigenlijk een input met een spatie erachter.
                value += " "
            if request == "en":  # Update english matrix with given pair
                if value[0] in self.alphabetkey and value[1] in self.alphabetkey:
                    self.enmatrice[self.alphabetkey.find(value[0])][self.alphabetkey.find(value[1])] += 1
                    self.total += 1
            elif request == "nl":  # Update dutch matrix with given pair
                if value[0] in self.alphabetkey and value[1] in self.alphabetkey:
                    self.nlmatrice[self.alphabetkey.find(value[0])][self.alphabetkey.find(value[1])] += 1
                    self.total += 1
            self.network.queue_message(Message(self,m.src,"PREDICTED",self.total))
