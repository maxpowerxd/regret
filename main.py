import multiprocessing
import random
from progress.bar import IncrementalBar

# Definitions
ROCK, PAPER, SCISSORS, NUM_ACTIONS = 0, 1, 2, 3
regret_sum = [0 for n in range(NUM_ACTIONS)]
strategy = [0.447, 0.193, 0.360]
strategy_sum = [0.447, 0.193, 0.360]
opp_strategy = [0.33334, 0.33333, 0.33333]


def get_strategy(regret_sum, strategy, strategy_sum):
    normalizing_sum = 0
    for a in range(NUM_ACTIONS):
        strategy[a] = regret_sum[a] if regret_sum[a] >= 0 else 0
        normalizing_sum += strategy[a]
    for a in range(NUM_ACTIONS):
        if normalizing_sum > 0:
            strategy[a] /= normalizing_sum
        else:
            strategy[a] = 1 / NUM_ACTIONS
        strategy_sum[a] += strategy[a]
    return regret_sum, strategy, strategy_sum


def get_action(strategy):
    r = random.random()
    a = 0
    cumulative_probability = 0
    while a < NUM_ACTIONS:
        cumulative_probability += strategy[a]
        if r < cumulative_probability:
            break
        a += 1
    return a


def train(iterations, regret_sum, strategy, strategy_sum):
    action_utility = [0 for n in range(NUM_ACTIONS)]
    bar = IncrementalBar('Countdown', max=iterations, suffix='%(percent)d%%'+' %(remaining)d')
    for i in range(iterations):
        # Get regret-matched mixed-strategy actions
        regret_sum, strategy, strategy_sum = get_strategy(regret_sum, strategy, strategy_sum)
        my_action = get_action(strategy)
        other_action = get_action(opp_strategy)

        # Compute action utilities
        action_utility[other_action] = 0
        # if other_action is scissors, rock (rock has the value 0) beats it
        action_utility[other_action + 1 if other_action < NUM_ACTIONS - 1 else 0] = +1
        # if other_action is rock, it beats scissors (scissors have the value 2)
        action_utility[other_action - 1 if other_action != 0 else 2] = -1
        # Accumulate action regrets
        for a in range(NUM_ACTIONS):
            regret_sum[a] += action_utility[a] - action_utility[my_action]
        bar.next()
    bar.finish()
    return strategy_sum
    # Get average mixed strategy across all training iterations


# Get average mixed strategy across all training iterations
def get_average_strategy(strategy_sum):
    avg_strategy = [0 for n in range(NUM_ACTIONS)]
    normalizing_sum = 0
    for a in range(NUM_ACTIONS):
        normalizing_sum += strategy_sum[a]
    for a in range(NUM_ACTIONS):
        if normalizing_sum > 0:
            avg_strategy[a] = strategy_sum[a] / normalizing_sum
        else:
            avg_strategy[a] = 1 / NUM_ACTIONS
    return avg_strategy

num_cores = multiprocessing.cpu_count()
strategy_sum = train(10, regret_sum, strategy, strategy_sum)
avg_strategy = get_average_strategy(strategy_sum)

print("The average strategy is: ", avg_strategy)
