import random

import utils
from pygame.locals import *
import math
import pygame
import time
from queue import PriorityQueue


class Controller:
    def __init__(self, drone, dmap):
        self.__drone = drone
        self.__dmap = dmap
        self.__start = False

    @staticmethod
    def generate_path(path, dest_x, dest_y):
        x = dest_x
        y = dest_y
        moves = [[x, y]]

        while len(path[(x, y)]):
            (x, y) = path[(x, y)]
            moves.append([x, y])
        return moves

    def start(self):
        # initialize the pygame module
        self.__dmap.loadMap("test1.map")
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("./assets/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((400, 400))
        screen.fill(utils.WHITE)

        dest_x = random.randint(0, 19)
        dest_y = random.randint(0, 19)

        while self.__dmap.surface[dest_x][dest_y] != 0 and dest_x != self.__drone.xCoordinate\
                and dest_y != self.__drone.yCoordinate:
            dest_x = random.randint(0, 19)
            dest_y = random.randint(0, 19)

        screen.blit(self.mapWithDrone(dest_x, dest_y, self.__dmap.image()), (0, 0))

        started_at = time.time()
        path = self.searchAStar(self.__dmap, self.__drone.xCoordinate, self.__drone.yCoordinate, dest_x, dest_y)
        print('-------------------------------------------------------')
        print('Path determined by A*: ', path)
        print("Execution time for A*: %s" % (time.time() - started_at))
        print('-------------------------------------------------------')
        screen.blit(self.displayPath(self.__dmap.image(), path, dest_x, dest_y), (0, 0))

        # started_at = time.time()
        # path = self.searchGreedy(self.__dmap, self.__drone.xCoordinate, self.__drone.yCoordinate, dest_x, dest_y)
        # print('-------------------------------------------------------')
        # print('Path determined by Greedy: ', path)
        # print("Execution time for Greedy: %s" % (time.time() - started_at))
        # print('-------------------------------------------------------')
        # screen.blit(self.displayPath(self.__dmap.image(), path, dest_x, dest_y), (0, 0))
        #
        # started_at = time.time()
        # path = self.simulated_annealing(10000, 10000, dest_x, dest_y)
        # print('-------------------------------------------------------')
        # print('Path determined by SA: ', path)
        # print("Execution time for SA: %s" % (time.time() - started_at))
        # print('-------------------------------------------------------')
        # screen.blit(self.displayPath(self.__dmap.image(), path, dest_x, dest_y), (0, 0))

        pygame.display.flip()
        time.sleep(1)

        # for move in reversed(path):
        #     self.__drone.xCoordinate = move[0]
        #     self.__drone.yCoordinate = move[1]
        #     screen.blit(self.mapWithDrone(dest_x, dest_y, self.__dmap.image()), (0, 0))
        #     screen.blit(self.displayPath(self.__dmap.image(), path, dest_x, dest_y), (0, 0))
        #     pygame.display.flip()
        #     time.sleep(0.25)

        for move in path:
            self.__drone.xCoordinate = move[0]
            self.__drone.yCoordinate = move[1]
            screen.blit(self.mapWithDrone(dest_x, dest_y, self.__dmap.image()), (0, 0))
            screen.blit(self.displayPath(self.__dmap.image(), path, dest_x, dest_y), (0, 0))
            pygame.display.flip()
            time.sleep(0.01)

        time.sleep(5)
        pygame.quit()

    def mapWithDrone(self, x, y, mapImage):
        flag = pygame.image.load("./assets/flag.png")
        mapImage.blit(flag, (y * 20, x * 20))
        drona = pygame.image.load("./assets/drona.png")
        mapImage.blit(drona, (self.__drone.yCoordinate * 20, self.__drone.xCoordinate * 20))

        return mapImage

    def simulated_annealing(self, temperature, iterations, dest_x, dest_y):

        x = self.__drone.xCoordinate
        y = self.__drone.yCoordinate
        cell = [x, y]
        moves = [cell]
        k = 0

        while k <= iterations:
            k += 1
            T = temperature / k
            if [x, y] == [dest_x, dest_y]:
                return moves
            # generate the neighbours of the drone
            neighbours = []

            for pos in utils.DIRECTIONS:
                new_x = x + pos[0]
                new_y = y + pos[1]

                if 0 <= new_x <= 19 and 0 <= new_y <= 19 and self.__dmap.surface[new_x][new_y] == 0:
                    neighbours.append([new_x, new_y])

            # pick a random neighbour
            next_cell = random.choice(neighbours)

            f1 = self.heuristic(next_cell[0], next_cell[1], dest_x, dest_y)
            f2 = self.heuristic(x, y, dest_x, dest_y)

            if f1 < f2:
                moves.append(next_cell)
                x = next_cell[0]
                y = next_cell[1]
            else:
                r = random.uniform(0, 1)
                E = f1 - f2

                if r < math.exp(E / T):
                    moves.append(next_cell)
                    x = next_cell[0]
                    y = next_cell[1]

        return moves

    def displayPath(self, image, path, dest_x, dest_y):
        mark = pygame.Surface((20, 20))
        mark.fill(utils.GREEN)
        for move in path:
            if move != [self.__drone.xCoordinate, self.__drone.yCoordinate]:
                image.blit(mark, (move[1] * 20, move[0] * 20))
                flag = pygame.image.load("./assets/flag.png")
                image.blit(flag, (dest_y * 20, dest_x * 20))
            else:
                flag = pygame.image.load("./assets/flag.png")
                image.blit(flag, (dest_y * 20, dest_x * 20))
                drona = pygame.image.load("./assets/drona.png")
                image.blit(drona, (self.__drone.yCoordinate * 20, self.__drone.xCoordinate * 20))

        return image

    @staticmethod
    def heuristic(initial_x, initial_y, final_x, final_y):
        return abs(initial_x - final_x) + abs(initial_y - final_y)

    def searchAStar(self, mapM, initialX, initialY, finalX, finalY):
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

            for position in utils.DIRECTIONS:
                new_x = x + position[0]
                new_y = y + position[1]

                if 0 <= new_x <= 19 and 0 <= new_y <= 19 and mapM.surface[new_x][new_y] == 0:
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

    def searchGreedy(self, mapM, initialX, initialY, finalX, finalY):
        # TO DO
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]
        moves = [[initialX, initialY]]
        heuristics_distances = {(initialX, initialY): 0, }  # represents the h function from the formula
        priority_queue = PriorityQueue()
        priority_queue.put((0, [initialX, initialY]))
        previous_cell = {(initialX, initialY): ()}

        while not priority_queue.empty():
            [x, y] = priority_queue.get()[1]

            for position in utils.DIRECTIONS:
                new_x = x + position[0]
                new_y = y + position[1]

                if 0 <= new_x <= 19 and 0 <= new_y <= 19 and mapM.surface[new_x][new_y] == 0:
                    if new_x == finalX and new_y == finalY:
                        previous_cell[(new_x, new_y)] = (x, y)
                        return self.generate_path(previous_cell, finalX, finalY)

                    new_h = self.heuristic(new_x, new_y, finalX, finalY)

                    if (new_x, new_y) not in heuristics_distances.keys() or  \
                            heuristics_distances[(new_x, new_y)] > new_h:
                        priority_queue.put((new_h, [new_x, new_y]))
                        heuristics_distances[(new_x, new_y)] = new_h
                        previous_cell[(new_x, new_y)] = (x, y)

        return []

