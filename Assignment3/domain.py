# -*- coding: utf-8 -*-

from random import *
from utils import *
import numpy as np
import pickle


# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation

# A gene represents in our context one of the 4 possible directions
class Gene:
    def __init__(self):
        # random initialise the gene according to the representation
        self.__gene = randint(0, 3)

    def get_value(self):
        return self.__gene

    def __eq__(self, other):
        return self.__gene == other.get_value()


# an individual represents a possible solution, and in our context, it means a possible path
class Individual:
    def __init__(self, size=0):
        self.__size = size
        self.__collection = [Gene() for _ in range(self.__size)]
        self.__fitness = None

    def get_fitness_value(self):
        return self.__fitness

    def convert_to_path(self, current_position, map):
        """
        We keep an array of the possible direction and we need the starting position
        of the drone in order to build the path
        :param current_position: the initial position of the drone.
        :param map: the map
        :return: the path as an array with coordinates of the cells
        """
        path = [(current_position[0], current_position[1])]
        for gene in self.__collection:
            next_x = path[-1][0] + DIRECTIONS[gene.get_value()][0]
            next_y = path[-1][1] + DIRECTIONS[gene.get_value()][1]

            # if map.valid_neighbour(next_x, next_y):
            #     path.append((next_x, next_y))

            path.append((next_x, next_y))

        return path

    def compute_fitness(self, map, current_position):
        """
        We compute the fitness of a possible solution:
            - if a gene in the individual is not valid, we skip it and decrease the score
            - if a gene in the individual is valid, we increment the fitness, and then for every
        cell that we can reach from that valid cell, we increment the fitness
        :param map: the given map
        :param current_position: the starting position of the drone
        :return: none
        """
        self.__fitness = 0

        path = self.convert_to_path(current_position, map)
        visited = []  # make sure not to go through the same cell, because they are generated randomly.

        for index in range(0, len(path)):
            x, y = path[index][0], path[index][1]

            # make sure that we don't visit the same block
            if (x, y) not in visited:
                if not map.valid_neighbour(x, y):
                    self.__fitness -= 15
                else:
                    self.__fitness += 1
                    visited.append((x, y))
                    # iterate in all 4 directions to explore as much as possible
                    for direction in DIRECTIONS:
                        new_x = x + direction[0]
                        new_y = y + direction[1]

                        while map.valid_neighbour(new_x, new_y):
                            if (new_x, new_y) not in visited:
                                visited.append((new_x, new_y))
                                self.__fitness += 1
                            new_x = new_x + direction[0]
                            new_y = new_y + direction[1]

    def mutate(self, current_position, map, mutate_probability=0.04):
        """
        Mutate means to change randomly a gene in the individual,
        and in order to do that we generate a new gene and replace a random index
        :param mutate_probability: the mutate probability
        :param current_position: the position of the drone
        :param map: the map
        :return: none
        """
        if random() < mutate_probability:
            index = randint(0, self.__size - 1)
            self.__collection[index] = Gene()
            self.compute_fitness(map, current_position)

    def crossover(self, other_parent, crossover_probability=0.8):
        """
        We create 2 children(offsprings) from 2 parents by aplying a fixed point.
        In this case we pick a random index, and then combine the halves of the parents in order
        to generate the children.
        :param other_parent: another individual object
        :param crossover_probability: the probability to apply a crossover
        :return: 2 individual objects that represents the generated children.
        """
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size)
        if random() < crossover_probability:
            index = randint(0, self.__size - 1)
            # perform the one point crossover between the self and the other parent.
            offspring1.__collection = self.__collection[:index] + other_parent.__collection[index:]
            offspring2.__collection = other_parent.__collection[:index] + self.__collection[index:]

        return offspring1, offspring2

# a population means a collection of possible solutions
class Population:
    def __init__(self, population_size=0, individual_size=0):
        self.__population_size = population_size
        self.__collection = [Individual(individual_size) for _ in range(population_size)]

    def add_individual(self, individual, map, current_position):
        self.__collection.append(individual)
        individual.compute_fitness(map, current_position)

    def get_average_fitness(self):
        fitness = []
        for individual in self.__collection:
            fitness.append(individual.get_fitness_value())

        return np.average(fitness)

    def get_population(self):
        return self.__collection

    def set_individuals(self, new_individuals):
        self.__collection = new_individuals

    def evaluate_individuals(self, map, current_position):
        # compute the fitness for every individual in the population.
        for individual in self.__collection:
            individual.compute_fitness(map, current_position)

    def selection(self, k=0):
        if k == 0:
            return []
        if k > len(self.__collection):
            k = len(self.__collection)

        # we sort the population by the fitness value of each individual,
        # and after that we select the best k individuals
        selected_individuals = sorted(self.__collection, key=lambda x: x.get_fitness_value(), reverse=True)
        return selected_individuals[:k]

    def get_best_path(self, map, current_position):
        """
        Returns the best path
        :param current_position: the initial position of the drone
        :param map: the given map
        :return: the best path
        """
        individuals = sorted(self.__collection, key=lambda x: x.get_fitness_value(), reverse=True)
        return individuals[0].convert_to_path(current_position, map)


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def random_map(self, fill=0.3):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1

    def valid_neighbour(self, x, y):
        if 0 <= x < self.n and 0 <= y < self.m and self.surface[x][y] != 1:
            return True
        return False

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def save_map(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def load_map(self, numFile):
        with open(numFile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()
