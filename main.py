from functions import get_event, paddedstrnum, computerparser, idtostrid, priorvalueparser, simparser
from computer import Proposer, Acceptor, Learner
from messages import Message
from network import Network

# Toch uiteindelijk besloten om alles te behandelen in main.
# Als we daar namelijk de functies en methodes gebruiken, kunnen we namelijk
# per tick ook gewoon een handeling uitvoeren.

def main(simfile:str):
    pass

def simulation(n_P: int, n_A: int, n_L: int, maxticks: int, E: list):
    # Initialise variables.
    # Proposals wordt bijgehouden in het Network object, waar alle proposers dan bij kunnen
    P = [Proposer(x+1,n_A,n_L) for x in range(n_P)]
    A = [Acceptor(y+1) for y in range(n_A)]
    L = [Learner(z+1) for z in range(n_L)]
    N = Network(P,A,L)
    # We sluiten het netwerk achteraf aan zodat we de proposers en acceptors in het netwerk kunnen stoppen ter referentie.
    for prop in P:
        prop.network = N
    for acc in A:
        acc.network = N
    for lrn in L:
        lrn.network = N
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
                print("{}: ** {} kapot **".format(paddedstrnum(tick,paddingnum),failc))
            for fixc in event[2]:  # Computers get repaired
                objfixc = computerparser(fixc,P,A)
                objfixc.failed = False
                print("{}: ** {} gerepareerd **".format(paddedstrnum(tick,paddingnum),fixc))
            if event[3] is not None and event[4] is not None:  # External agent wants to propose new value.
                # print(event[3])
                targetc = N.find_proposer(event[3] - 1)
                m = Message(None,targetc,"PROPOSE",event[4])
                targetc.handle_external_message(m)
                print("{}: {} -> {}  {} {}".format(paddedstrnum(tick,paddingnum),"  ","P{}".format(event[3]),"PROPOSE",event[4]))
        else:
            m = N.extract_message()
            if m is not None:
                if m.type == "PROMISE":  # m.dst is P, m.src is A
                    print("{}: {} -> {}  {} n={} {}".format(paddedstrnum(tick,paddingnum),idtostrid(m.src),idtostrid(m.dst),m.type,m.dst.proposalid,priorvalueparser(m.src.prevpropid,m.src.value)))
                elif m.type == "ACCEPTED":  # m.dst is P, m.src is A
                    print("{}: {} -> {}  {} n={} v={}".format(paddedstrnum(tick,paddingnum),idtostrid(m.src),idtostrid(m.dst),m.type,m.dst.proposalid, m.value))
                elif m.type == "ACCEPT":  # m.dst is A, m.src is P
                    print("{}: {} -> {}  {} n={} v={}".format(paddedstrnum(tick,paddingnum),idtostrid(m.src),idtostrid(m.dst),m.type,m.src.proposalid, m.value))
                elif m.type == "PREPARE":  # m.dst is A, m.src is P
                    print("{}: {} -> {}  {} n={}".format(paddedstrnum(tick,paddingnum),idtostrid(m.src),idtostrid(m.dst),m.type,m.src.proposalid))
                elif m.type == "REJECTED":  # m.dst is P, m.src is A
                    print("{}: {} -> {}  {} n={}".format(paddedstrnum(tick,paddingnum),idtostrid(m.src),idtostrid(m.dst),m.type,m.dst.proposalid))
                elif m.type == "SUCCESS":  # m.dst is L, m.src is P
                    print("{}: {} -> {}  {} v={}".format(paddedstrnum(tick,paddingnum),idtostrid(m.src),idtostrid(m.dst),m.type,m.value))
                elif m.type == "PREDICTED":
                    print("{}: {} -> {}  {} n={}".format(paddedstrnum(tick,paddingnum),idtostrid(m.src),idtostrid(m.dst),m.type,m.value))
                m.dst.process_message(m)
            else:  # Er wordt niks gedaan op het moment.
                print("{}:".format(paddedstrnum(tick, paddingnum)))

    # Simulatie klaar, consensus evalueren per proposer.
    print("\n")
    for proposer in P:
        print("Proposer {} proposed the following:\n".format(proposer.id))
        for i in range(len(proposer.historyproposed)):
            print("Proposed: {}, Accepted: {}, Consensus reached: {}".format(proposer.historyproposed[i],proposer.historyaccepted[i],proposer.historyreached[i]))
        print("")

if __name__ == "__main__":
    parser = simparser("test-3")
    simulation(parser[0],parser[1],parser[2],parser[3],parser[4])
