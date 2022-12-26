from kaggle_environments import make
from kaggle_environments.envs.hungry_geese import hungry_geese as hg
import logging
import hg_agent_1
import hg_agent_2

logging.basicConfig(format="", filename="hg.txt", filemode="w", level=logging.DEBUG)
logger = logging.getLogger()

config = dict(rows=5, columns=10)

env = make("hungry_geese", config, debug=True)

#print(env.agents)

game = env.run([hg_agent_2.agent, hg_agent_2.agent])

print(game[0][0])

for step in game:
    logger.info(f"Step: {[step[0].observation.step]}")
    logger.info(hg.renderer(step, env))
    logger.info(f"Actions: {[agent.action for agent in step]}")
    logger.info(f"Geese: {[step[0].observation.geese]}")
    logger.info(f"Food: {[step[0].observation.food]}")