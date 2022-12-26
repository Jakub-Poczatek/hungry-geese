from kaggle_environments.envs.hungry_geese import hungry_geese as hg
import numpy.random as rng
import hg_helpers as h

cached_agents = {}

class SelfAvoidingAgent:

    def __init__(self,config):
        self.config = hg.Configuration(config)
        self.prev_action = None

    def __call__(self,obs):
        actions = h.ACTIONS.copy()
        player = obs.index
        head = obs.geese[player][0]

        if self.prev_action:
            actions.remove(h.reverseDirection(self.prev_action))

        #Step 2 - avoid own body and other geese
        for action in actions:
            if(h.neightbours(head, [action], self.config) in obs.geese[player]):
                actions.remove(action)

        #Step 3 - be greedy (with wrap around)
        #Step 4 - do 1-step look ahead

        minFood = obs.food[0]
        minDist, _ = h.min_distance(head, minFood, self.config)

        for food in obs.food:
            tempDist, _ = h.min_distance(head, food, self.config)
            if tempDist < minDist: 
                minDist = tempDist
                minFood = food

        _, moves = h.min_distance(head, minFood, self.config)

        #for move in moves:
            #if move in actions:
                #self.prev_action = move

        self.prev_action = rng.choice(actions)
        return self.prev_action

#s = SelfAvoidingAgent(config)

def agent(obs,config):
    global cached_agents

    obs = hg.Observation(obs)
    player = obs.index
    
    if player not in cached_agents:
        cached_agents[player] = SelfAvoidingAgent(config)
    
    return cached_agents[player](obs)