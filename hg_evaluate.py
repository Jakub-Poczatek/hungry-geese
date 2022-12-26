from kaggle_environments import evaluate
import hg_agent_1 as agent_1
import hg_agent_2 as agent_2

runs = evaluate('hungry_geese', [agent_2.agent, agent_1.agent], num_episodes=100)

#print(runs)

# f = first agent, s = second agent
first_win_count = len([1 for f,s in runs if f>s])
second_win_count = len([1 for f,s in runs if f<s])

print(first_win_count, second_win_count)