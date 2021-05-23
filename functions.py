"""Contains all the functions for manipulating events which will be used in the simulation
function in main.py. This has been decided so that we can limit one operation per tick."""
from events import Event

### CHECKLIST ###
# (Tijdelijk, wordt na ontwikkeling weggehaald)
# [] queue_message(N,m)
# [] extract_message(N)
#
#
#
#
#

### HELPER ###

def simparser(instructionsfile:str):
    """Parses an instruction file for use in the simulation.
    Said file should consist of the following;
    First rule: n_p, n_a, tmax
    Next rules: events (see events.py)"""
    with open(instructionsfile) as infile:
        instructions = list(map(str.strip,infile.readlines()))
    line1 = instructions[0].split(' ')
    if len(line1) == 3:  # Simulation expects 3 parameters.
        try:
            n_p, n_a, tmax = int(line1[0]), int(line1[1]), int(line1[2])
        except:
            raise Exception("Failure converting first rule to numbers. Check if it contains only numbers (0-9),\n"
                            "and no additional whitespaces. Example: 'n_P n_A tmax'")
    else:
        raise Exception("First rule in instruction file does not follow conventions;\n"
                        "First number should contain amount of proposers.\n"
                        "Second number should contain amount of acceptors.\n"
                        "Third number declares tmax for simulation.\n")
    events = instructions[1:]
    eventdict = {}
    for event in events:  # Gets a single rule from the remaining inputs.
        readstatus = 0  # FSM-ish method of reading instructions and classifying them.
        eventblocks = event.split(' ')
        try:
            tick = int(eventblocks[0])
        except:
            raise Exception("Error converting event tick info. Tick = {}".format(text))
        if tick not in eventdict.keys():  # New event, create template.
            eventdict[tick] = [tick,[],[],None,None]  # (t, failedcomputers, repairedcomputers, proposerid, proposervalue)
        e = eventdict[tick]  # Edit the event.
        for text in eventblocks[1:]:  # Evaluates each word in each rule.
            if readstatus == 0:  # Awaiting event type.
                if text.upper() == "PROPOSE":  # Expecting proposer id and proposer value.
                    readstatus = 1
                elif text.upper() == "FAIL":
                    readstatus = 3
                elif text.upper() == "RECOVER":
                    readstatus = 7
                elif text.upper() == "END":  # Ignore entire rule.
                    readstatus = 11
            elif readstatus == 1:  # Awaiting proposerid.
                try:
                    proposerid = int(text)
                    readstatus = 2
                except:
                    raise Exception("Error converting event proposerid. Proposerid = {}".format(text))

            elif readstatus == 2:  # Awaiting proposervalue
                try:
                    proposervalue = int(text)
                    e[3] = proposerid
                    e[4] = proposervalue
                    eventdict[tick] = e  # Commit.
                    readstatus = 11  # Done, revert to end state.
                except:
                    raise Exception("Error converting event proposervalue. Proposervalue = {}".format(text))

            elif readstatus == 3:  # Awaiting computer type for fail event
                try:
                    comptype = str(text)
                    if comptype.upper() == "PROPOSER":
                        readstatus = 4
                    elif comptype.upper() == "ACCEPTOR":
                        readstatus = 5
                    # elif comptype.upper() == "LEARNER":
                    #   readstatus = 6
                except:
                    raise Exception("Error converting fail event computertype. Computertype = {}".format(text))

            elif readstatus == 4:  # Awaiting proposer ID.
                try:
                    proposerfailid = str(text)
                    e[1].append("{}{}".format("P",proposerfailid))
                    eventdict[tick] = e
                    readstatus = 11
                except:
                    raise Exception("Error converting event proposerfailid. Proposerfailid = {}".format(text))

            elif readstatus == 5:  # Awaiting proposer ID.
                try:
                    acceptorfailid = str(text)
                    e[1].append("{}{}".format("A",acceptorfailid))
                    eventdict[tick] = e
                    readstatus = 11
                except:
                    raise Exception("Error converting event acceptorfailid. Acceptorfailid = {}".format(text))

            # 6 reserved for learner.

            elif readstatus == 7:
                try:
                    comptype = str(text)
                    if comptype.upper() == "PROPOSER":
                        readstatus = 8
                    elif comptype.upper() == "ACCEPTOR":
                        readstatus = 9
                    # elif comptype.upper() == "LEARNER":
                    #   readstatus = 10
                except:
                    raise Exception("Error converting recover event computertype. Computertype = {}".format(text))

            elif readstatus == 8:  # Awaiting proposer ID.
                try:
                    proposerrepid = str(text)
                    e[2].append("{}{}".format("P",proposerrepid))
                    eventdict[tick] = e
                    readstatus = 11
                except:
                    raise Exception("Error converting event proposerrepid. Proposerrepid = {}".format(text))

            elif readstatus == 9:  # Awaiting acceptor ID.
                try:
                    acceptorrepid = str(text)
                    e[2].append("{}{}".format("A",acceptorrepid))
                    eventdict[tick] = e
                    readstatus = 11
                except:
                    raise Exception("Error converting event acceptorrepid. Acceptorrepid = {}".format(text))

            # 10 reserved for learner.

            elif readstatus == 11:  # Already processed a full event this rule.
                continue

    # Done parsing. Convert events to a list, do the same for the sim params.
    eventlist = []
    for key in eventdict.keys():
        eventlist.append(eventdict[key])

    return n_p, n_a, tmax, eventlist

def determinenumdepth(num:int or float):
    """Recursively determines the significance of a given number before
    the dot."""
    if num >= 1:
        return 1 + determinenumdepth(num/10)
    else:
        return 0

def paddedstrnum(num:int, highnum:int) -> str:
    """Returns num as string, padded to be on the same length with the highest num value."""
    padded = ""
    strnum = str(num)
    numlen = determinenumdepth(num)
    maxlen = determinenumdepth(highnum)
    padlen = maxlen - numlen
    for i in range(padlen):
        padded += "0"
    for j in range(len(strnum)):
        padded += "{}".format(strnum[j])
    return padded

### EVENTS ###

def extract_event(eventqueue, simtick):
    for e in eventqueue:  # Itereert over Event objecten.
        if e.tick == simtick:
            return e
    return None  # Geen event gevonden voor de huidige tick.

### NETWORK ###
def queue_message(network, message):
    network.messagequeue.append(message)

def extract_message(network):
    for m in network.messagequeue:
        if m.src.failed == False and m.dst.failed == False:
            return m
    return None