# Copyright 2019 George Le
from searchagent import SearchAgent

def grade(agent):
    return (100 * agent.successful_return()) + (100 * agent.target_found()) + (5 * agent.steps()) - agent.num_repeats()