# -*- coding: utf-8 -*-

import pickle
from domain import *


class Repository:
    def __init__(self):
        self.__populations = []
        self.__map = Map()
        self.__current_position = self.random_current_position()

    def add_population(self, population):
        self.__populations.append(population)

    def add_individual(self, individual):
        # add an individual to the current population
        self.__populations[-1].add_individual(individual, self.__map, self.__current_position)

    def set_population(self, new_population):
        self.__populations[-1].set_individuals(new_population)

    def create_population(self, args):
        # args = [populationSize, individualSize] -- you can add more args
        return Population(args[0], args[1])

    def evaluate_population(self):
        # evaluate all the individuals of the current population
        return self.__populations[-1].evaluate_individuals(self.__map, self.__current_position)

    def make_selection(self, size):
        """
        select the best individuals from the current population
        :param size: size of the population
        :return: an array of individuals
        """
        return self.__populations[-1].selection(size)

    def get_best_path(self):
        # we return the best path from the population with the highest fitness average
        ordered_populations = sorted(self.__populations, key=lambda x: x.get_average_fitness(), reverse=True)
        return ordered_populations[0].get_best_path(self.__current_position)

    def get_current_population(self):
        return self.__populations[-1].get_population()

    def get_average_fitness(self):
        return self.__populations[-1].get_average_fitness()

    def create_random_map(self):
        self.__map.random_map()

    def load_map(self, file):
        self.__map.load_map(file)

    def save_map(self, file):
        self.__map.save_map(file)

    def get_map(self):
        return self.__map

    def random_current_position(self):
        x = randint(0, self.__map.n - 1)
        y = randint(0, self.__map.m - 1)
        while self.__map.surface[x][y] != 0:
            x = randint(0, self.__map.n - 1)
            y = randint(0, self.__map.m - 1)
        return [x, y]
