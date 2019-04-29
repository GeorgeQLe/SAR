# Copyright 2019 George Le
from searchagent import SearchAgent

def grade(agent):
    print(agent.path_taken())
    return (100 * agent.targets_found()) + (5 * agent.steps()) - agent.num_of_repeats() - (5 * agent.invalid_moves())