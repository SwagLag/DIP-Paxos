from network import Network
from computer import Computer

# Toch uiteindelijk besloten om alles te behandelen in main.
# Als we daar namelijk de functies en methodes gebruiken, kunnen we namelijk
# per tick ook gewoon een handeling uitvoeren.

def

def simulation(n_P: int, n_A: int, maxticks: int, E: list):
    # Initialise variables.
    proposals = 1
    N = []
    P = [Computer(x, N) for x in range(n_P)]
    A = [Computer(y, N) for y in range(n_A)]
    # Begin simulation.
    for tick in range(maxticks):
        event = getevent(E)
