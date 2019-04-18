# Copyright 2019 George Le
from sys import argv

from file import valid_directory, add_endslash
from geneticalgorithm import GeneticAlgorithm
from searchagent import SearchAgent

def main():
    debug = "NONE"
    path = "./Dumps"
    if len(argv) > 1:
        debug = argv[1] # the first command line argument should be whether or not the 
                        # user wishes to have the program output helpful debug text to
                        # the files designated in debug_output_files.txt
        if debug != "NONE" and debug != "ALL":
            print("ERROR: first argument should be a choice about the debug!")
        path = argv[2]
        if not valid_directory(path):
            print("ERROR:", path, "is not a valid path!")
            
    ga = GeneticAlgorithm()
    ga.run(layers_info= dict({
            0 : (9, 5),
            1 : (5, 1)
            }), 
            num_generations= 1, 
            number_of_individuals= 5, 
            number_of_individual_genes= 50)

if __name__ == "__main__":
    main()