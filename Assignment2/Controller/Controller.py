import utils
from pygame.locals import *
from Model.Drone import Drone
from Model.Map import Map
from random import randint
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
        logo = pygame.image.load("assets/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((400, 400))
        screen.fill(utils.WHITE)

        # define a variable to control the main loop
        running = True


        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False

                if event.type == KEYDOWN:
                    self.move(self.__dmap)  # this call will be erased

            screen.blit(self.mapWithDrone(self.__dmap.image()), (0, 0))
            pygame.display.flip()

        # path = self.searchAStar(self.__dmap, self.__drone.xCoordinate, self.__drone.yCoordinate, 4, 0)
        # screen.blit(self.displayWithPath(self.__dmap.image(), path), (0, 0))
        greedy_path = self.searchGreedy(self.__dmap, self.__drone.xCoordinate, self.__drone.yCoordinate, 4, 0)
        screen.blit(self.displayWithPath(self.__dmap.image(), greedy_path), (0, 0))
        pygame.display.flip()

        time.sleep(5)
        pygame.quit()

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.__drone.xCoordinate > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.__drone.xCoordinate - 1][self.__drone.yCoordinate] == 0:
                self.__drone.xCoordinate = self.__drone.xCoordinate - 1
        if self.__drone.xCoordinate < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.__drone.xCoordinate + 1][self.__drone.yCoordinate] == 0:
                self.__drone.xCoordinate = self.__drone.xCoordinate + 1

        if self.__drone.yCoordinate > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.__drone.xCoordinate][self.__drone.yCoordinate - 1] == 0:
                self.__drone.yCoordinate = self.__drone.yCoordinate - 1
        if self.__drone.yCoordinate < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.__drone.xCoordinate][self.__drone.yCoordinate + 1] == 0:
                self.__drone.yCoordinate =self.__drone.yCoordinate + 1

    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (self.__drone.yCoordinate * 20, self.__drone.xCoordinate * 20))

        return mapImage

    def displayWithPath(self, image, path):
        mark = pygame.Surface((20, 20))
        mark.fill(utils.GREEN)
        for move in path:
            image.blit(mark, (move[1] * 20, move[0] * 20))

        return image

    @staticmethod
    def heuristic(initial_x, initial_y, final_x, final_y):
        return abs(initial_x - final_x) + abs(initial_y - final_y)

    def searchAStar(self, mapM, initialX, initialY, finalX, finalY):
        # TO DO
        # implement the search function and put it in controller
        # returns a list of moves as a list of pairs [x,y]
        moves = [[initialX, initialY]]
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

