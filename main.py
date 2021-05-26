from functions import get_event, paddedstrnum, computerparser, idtostrid, priorvalueparser, simparser
from computer import Proposer, Acceptor
from messages import Message
from network import Network

# Toch uiteindelijk besloten om alles te behandelen in main.
# Als we daar namelijk de functies en methodes gebruiken, kunnen we namelijk
# per tick ook gewoon een handeling uitvoeren.

def main(simfile:str):
    pass

def simulation(n_P: int, n_A: int, maxticks: int, E: list):
    # Initialise variables.
    # Proposals wordt bijgehouden in het Network object, waar alle proposers dan bij kunnen
    P = [Proposer(x+1,n_A) for x in range(n_P)]
    A = [Acceptor(y+1) for y in range(n_A)]
    N = Network(P,A)
    # We sluiten het netwerk achteraf aan zodat we de proposers en acceptors in het netwerk kunnen stoppen ter referentie.
    for prop in P:
        prop.network = N
    for acc in A:
        acc.network = N
    paddingnum = max([999,maxticks])
    # Begin simulation.
    for tick in range(maxticks):
        if len(N.messagequeue) == 0 and len(E) == 0:
            break
        event = get_event(E, tick)
        if event is not None:
            # Process event.
            # Event structure as follows:
            # [ticks, [listoffailingcomputers], [listoffixedcomputers], proposerid, proposervalue]
            for failc in event[1]:  # Computers fail
                objfailc = computerparser(failc,P,A)
                objfailc.failed = True
                print("** {} kapot **".format(failc))
            for fixc in event[2]:  # Computers get repaired
                objfixc = computerparser(fixc,P,A)
                objfixc.failed = False
                print("** {} gerepareerd **".format(fixc))
            if event[3] is not None and event[4] is not None:  # External agent wants to propose new value.
                # print(event[3])
                targetc = N.find_proposer(event[3] - 1)
                m = Message(None,targetc,"PROPOSE",event[4])
                targetc.handle_external_message(m)
                print("{}: {} -> {}  {} {}".format(paddedstrnum(tick,paddingnum),"  ","P{}".format(event[3]),"PROPOSE",event[4]))
        else:
            m = N.extract_message()
            if m is not None:
                print("{}: {} -> {}  {} {}".format(paddedstrnum(tick,paddingnum),idtostrid(m.src),idtostrid(m.dst),m.type,priorvalueparser(None,None)))
                m.dst.process_message(m)
            else:
                print("{}:".format(paddedstrnum(tick, paddingnum)))

if __name__ == "__main__":
    parser = simparser("test-1")
    simulation(parser[0],parser[1],parser[2],parser[3])
