import pickle
from queue import PriorityQueue
from random import random, randint
import numpy as np
import pygame
from utils import *


class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
        self.random_map()

    def generate_drone_initial_position(self):
        x = randint(0, self.n - 1)
        y = randint(0, self.m - 1)

        while self.surface[x][y] != 0:
            x = randint(0, self.n - 1)
            y = randint(0, self.m - 1)

        return x, y

    def get_map(self):
        return self.surface

    def random_map(self, fill=0.20):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j] = 1


    @staticmethod
    def generate_path(path, dest_x, dest_y):
        x = dest_x
        y = dest_y
        moves = [[x, y]]

        while len(path[(x, y)]):
            (x, y) = path[(x, y)]
            moves.append([x, y])
        return moves

    @staticmethod
    def heuristic(initial_x, initial_y, final_x, final_y):
        return abs(initial_x - final_x) + abs(initial_y - final_y)

    def searchAStar(self, initialX, initialY, finalX, finalY):
        # TO DO
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]
        distances = {(initialX, initialY): 0, }  # represents the g function from the formula
        heuristics_distances = {(initialX, initialY): 0, }  # represents the h function from the formula
        priority_queue = PriorityQueue()
        priority_queue.put((0, [initialX, initialY]))
        previous_cell = {(initialX, initialY): ()}

        while not priority_queue.empty():
            [x, y] = priority_queue.get()[1]

            for position in DIRECTIONS:
                new_x = x + position[0]
                new_y = y + position[1]

                if 0 <= new_x <= 19 and 0 <= new_y <= 19 and self.surface[new_x][new_y] != 1:
                    if new_x == finalX and new_y == finalY:
                        previous_cell[(new_x, new_y)] = (x, y)
                        return self.generate_path(previous_cell, finalX, finalY)

                    new_g = 1 + distances[(x, y)]
                    new_h = self.heuristic(new_x, new_y, finalX, finalY)

                    new_f = new_g + new_h

                    if (new_x, new_y) not in distances.keys() or distances[(new_x, new_y)] + \
                            heuristics_distances[(new_x, new_y)] > new_f:
                        priority_queue.put((new_f, [new_x, new_y]))
                        distances[(new_x, new_y)] = new_g
                        heuristics_distances[(new_x, new_y)] = new_h
                        previous_cell[(new_x, new_y)] = (x, y)

        return []

    def valid_neighbour(self, x, y):
        if 0 <= x < self.n and 0 <= y < self.m and self.surface[x][y] != 1:
            return True
        return

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def saveMap(self, numFile="test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numFile):
        with open(numFile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def image(self, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine

    def get_cell(self, x, y):
        return self.surface[x][y]

    def set_cell(self, x, y, value):
        self.surface[x][y] = value
