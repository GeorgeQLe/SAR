# Copyright 2019 George Le

from searchagent import SearchAgent

def grade(agent):
    return (10 * agent.targets_found()) - (5 * agent.falsepos_found()) + agent.steps() - agent.num_of_repeats() - agent.invalid_moves() - (50 * agent.random_choices())