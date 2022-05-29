import numpy as np

import gui
from repository import *
from gui import *

class Controller:
    def __init__(self, repository):
        # args - list of parameters needed in order to create the controller
        self.__repository = repository
        self.population_size = 30
        self.individual_size = 10
        self.runs = 30
        self.iterations_count = 150
        self.mutate_probability = 0.04
        self.crossover_probability = 0.8
        self.statistics_info = []

    def set_population_size(self, new_value):
        self.population_size = new_value

    def set_individual_size(self, new_value):
        self.individual_size = new_value

    def set_runs(self, new_value):
        self.runs = new_value

    def set_iterations(self, new_value):
        self.iterations_count = new_value

    def set_mutate_probability(self, new_value):
        self.mutate_probability = new_value

    def set_crossover_probability(self, new_value):
        self.crossover_probability = new_value

    def generate_random_map(self):
        self.__repository.create_random_map()

    def load_map(self, file):
        self.__repository.load_map(file)

    def save_map(self, file):
        self.__repository.save_map(file)

    def get_map(self):
        return self.__repository.get_map()

    def view_map(self):
        print('Map: ')
        print(self.__repository.get_map())
        gui.movingDrone(self.__repository.get_map(), [])

    def iteration(self):
        # args - list of parameters needed to run one iteration
        # an iteration:
        # selection of the parents
        # create offsprings by crossover of the parents
        # apply some mutation s
        # selection of the survivors

        # compute the fitness function for the entire population
        parents_selection = self.__repository.make_selection(self.population_size)
        parents_length = len(parents_selection)

        halve_one = parents_selection[: (parents_length // 2)]
        halve_two = parents_selection[(parents_length // 2):]
        pairs = []
        for _ in range(parents_length // 2):
            first_parent = halve_one[randint(0, (parents_length // 2) - 1)]
            second_parent = halve_two[randint(0, (parents_length // 2) - 1)]
            # apply crossover on half of the parents.
            if (first_parent, second_parent) not in pairs:
                pairs.append((first_parent, second_parent))
                offspring1, offspring2 = first_parent.crossover(second_parent, self.crossover_probability)
                offspring1.mutate(self.__repository.get_current_position(), self.__repository.get_map(), self.mutate_probability)
                offspring2.mutate(self.__repository.get_current_position(), self.__repository.get_map(), self.mutate_probability)
                self.__repository.add_individual(offspring1)
                self.__repository.add_individual(offspring2)

        # keep only the survivors...the individuals with the best fitness
        self.__repository.set_population(self.__repository.make_selection(self.population_size))

    def run(self):
        # args - list of parameters needed in order to run the algorithm
        
        # until stop condition
        #    perform an iteration
        #    save the information need it for the satistics
        
        # return the results and the info for statistics

        # compute the average fitness for an interation
        average_fitness = []
        for _ in range(0, self.iterations_count):
            self.iteration()
            average_fitness.append(self.__repository.get_average_fitness())

        self.statistics_info.append((np.average(average_fitness), np.std(average_fitness)))
    
    def solver(self):
        # args - list of parameters needed in order to run the solver
        
        # create the population,
        # run the algorithm
        # return the results and the statistics
        for index in range(0, self.runs):
            seed(index)  # change the seed every run to avoid possible duplicates
            population = self.__repository.create_population((self.population_size, self.individual_size))
            self.__repository.add_population(population)
            self.__repository.evaluate_population()
            self.run()

        return self.__repository.get_best_path(), self.statistics_info
       