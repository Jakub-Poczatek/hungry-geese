# utility functions to support AI of agents
from kaggle_environments.envs.hungry_geese import hungry_geese as hg
import numpy.random as rng

ACTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]

def reverseDirection(action):
    return ACTIONS[(ACTIONS.index(action)+2)%4]

def rc_to_cell(row, col, config):
    return (row*config["columns"]) + col

def cell_to_rc(cell, config):
    return cell//config["columns"], cell % config["columns"]

def neightbours(cell, actions, config):
    # Return a dict of ACTION:cell for each action in ACTIONS

    temp = {
        "NORTH": {"c": 0, "r" : -1},
        "EAST": {"c": 1, "r" : 0},
        "SOUTH": {"c": 0, "r" : 1},
        "WEST": {"c": -1, "r" : 0}
    }

    res = {}
    for action in actions:
        r, c = cell_to_rc(cell, config)
        c += temp[action]["c"]
        r += temp[action]["r"]
        res[action] = rc_to_cell(r%config["rows"], c%config["columns"], config)
    
    return res

    #return { action: cell + temp[action] for action in actions }

def _1D_min_distance(src, dest, size, direction):
    #Determine min distance from src to dest (allowing warpping based on size). 
    if src == dest: return 0, None

    wrap_dest = dest + (1 if src>dest else -1) * size

    if abs(wrap_dest - src) < abs(dest-src):
        return abs(wrap_dest - src), direction if src < wrap_dest else reverseDirection(direction)
    else:
        return abs(dest-src), direction if src < dest else reverseDirection(direction)

    # return dist and wrap
    return 0, False

def min_distance(src_cell, dest_cell, config):
    # Return min distance and h- and v- direection needed to go from src_cell to dest_cell
    # (wrapping allowed)

    #if(src_cell==dest_cell): return 0, []
    src_r, src_c = cell_to_rc(src_cell, config)
    dest_r, dest_c = cell_to_rc(dest_cell, config)
    dist_r, dir_r = _1D_min_distance(src_r, dest_r, config.rows, "SOUTH")
    dist_c, dir_c = _1D_min_distance(src_r, dest_r, config.rows, "EAST")
    return dist_r + dist_c, [d for d in [dir_r, dir_c] if d is not None] 

if __name__ == "__main__":
    print("Testing reverseDirection...")
    assert reverseDirection("NORTH") == "SOUTH"
    assert reverseDirection("SOUTH") == "NORTH"
    assert reverseDirection("EAST") == "WEST"
    assert reverseDirection("WEST") == "EAST"

    print("Testing rc_to_cell and cell_to_rc...")
    config = hg.Configuration({"rows": 5, "columns": 10})
    for cell in range(config.rows*config.columns):
        assert rc_to_cell(*cell_to_rc(cell, config), config) == cell

    print("Testing neighbours...")
    assert neightbours(0, ["EAST"], config)["EAST"] == 1
    assert neightbours(0, ["EAST"], config) == {"EAST": 1}
    assert neightbours(0, ["WEST"], config)["WEST"] == config.columns-1
    assert neightbours(0, ["NORTH"], config)["NORTH"] == (config.rows-1) * (config.columns)

    print("Testing _1D_min_distance...")
    src = 2
    for dest in range(config.columns):
        dist, dir = _1D_min_distance(src, dest, config.columns, "EAST")
        print(f"{src=:2d} \t {dest=:2d} => {dist=:2d} \t {dir=}")

    print("Testing min_distance...")
    for k in range(10):
        src_cell, dest_cell = rng.randint(config.rows * config.columns, size=2)
        dist, dir = min_distance(src_cell, dest_cell, config)
        print(f"{src_cell=:2d} \t {dest_cell=:2d} \t {dist=:2d}, {dir=}")

    
