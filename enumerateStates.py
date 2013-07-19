
from numpy import zeros

def enumerateStates(num_sites):
    """
    Enumerates all states possible for some number of binary sites.
    """

    num_states = 2**num_sites

    all_states = zeros(shape=(num_states,num_sites),dtype="int") 

    for i in range(num_sites-1,-1,-1):
        interval = 2**(i)
        state = 1
        for q in range(num_states):
            if q % interval == 0:
                if state == 0:
                    state = 1
                else:
                    state = 0
            all_states[q,i] = state

    return all_states

