# Copyright 2019 George Le

from searchagent import SearchAgent

def grade(self, agent = SearchAgent()):
    return (10 * agent.targets_found()) - (5 * agent.falsepos_found()) - (5 * agent.empty_fuel()) - agent.steps() - agent.turns_taken() - (2 * agent.num_of_repeats())