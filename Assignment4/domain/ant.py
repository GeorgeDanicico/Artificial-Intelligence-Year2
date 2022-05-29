import random
from utils import *

import numpy as np

class Ant:
    def __init__(self, size, battery):
        self.size = size
        self.path = [random.randint(0, size - 1)]
        self.fitness = 0
        self.battery = battery

    def __get_possible_moves(self, distances):
        """
        Returns a list of valid possible moves
        :param distances: matrix that contains the distances from a sensor to another(as a graph)
        :return: moves -> list of possible moves.
        """
        moves = []
        # each sensor is represented by an index
        # the path will contain only the order of the sensors
        current_sensor = self.path[-1]

        for next_sensor in range(self.size):
            if next_sensor != current_sensor and distances[current_sensor][next_sensor] != INF and\
                    next_sensor not in self.path and self.battery >= distances[current_sensor][next_sensor]:
                moves.append(next_sensor)
        return moves

    def __probability_to_choose_next_sensor(self, moves, alpha, beta, distances, pheromones):
        """
        Returns the probability to choose the next sensor
        :param moves: the order of next possible sensors
        :param alpha:
        :param beta:
        :param distances: the matrix that contains the distances between sensors
        :param pheromones: the pheromones matrix
        :return: the probability to cgoose the next sensor
        """
        current_sensor = self.path[-1]
        next_sensor_probability = [0 for _ in range(self.size)]

        for i in moves:
            distance_to_next_sensor = distances[current_sensor][i]
            pheromone_of_next_sensor = pheromones[current_sensor][i]
            prob = (distance_to_next_sensor ** beta) * (pheromone_of_next_sensor ** alpha)
            next_sensor_probability[i] = prob

        return next_sensor_probability

    def next_move(self, distances, pheromones, q0, alpha, beta):
        """
        Returns the next sensor to pick
        :param distances: the distance matrix
        :param pheromones: the pheromones matrix
        :param q0: the probability to choose the best possible move
        :param alpha:
        :param beta:
        :return:
        """
        moves = self.__get_possible_moves(distances)
        if not moves:
            return False

        next_cell_probability = self.__probability_to_choose_next_sensor(moves, alpha, beta, distances, pheromones)
        if random.random() < q0:
            # best_choice represents the best probability
            best_choice = max(next_cell_probability)
            selected_cell = next_cell_probability.index(best_choice)
        else:
            selected_cell = self._roulette(next_cell_probability)

        self.battery -= distances[self.path[-1]][selected_cell]
        self.path.append(selected_cell)

        return True

    def _roulette(self, next_cell_probability):
        """
        Selects randomly a sensor
        :param next_cell_probability: probabilities to pick the next sensor
        :return:
        """
        # probabilities represents the sum of the next sensor probability
        probabilities = sum(next_cell_probability)

        if probabilities == 0:
            return random.randint(0, len(next_cell_probability) - 1)

        probs_sum = [next_cell_probability[0] / probabilities]
        for i in range(1, self.size):
            probs_sum.append(probs_sum[i - 1] + next_cell_probability[i] / probabilities)

        r = random.random()
        position = 0
        while r > probs_sum[position]:
            position += 1
        return position

    def compute_fitness(self, distances):
        """
        Fitness is represented by the total distance that the ant traversed
        :param distances: matrix that represents the distances between sensors.
        :return: void
        """
        length = 0
        for i in range(1, len(self.path)):
            length += distances[self.path[i - 1]][self.path[i]]

        self.fitness = length

    def get_fitness(self):
        return self.fitness

    def get_path(self):
        return self.path

    def get_battery(self):
        return self.battery