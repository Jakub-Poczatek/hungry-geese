import numpy.random as rng

def agent (obs,config):
    return "EAST" if rng.uniform() < 0.1 else "NORTH"