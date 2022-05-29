import utils
from Model.Environment import Environment
from Model.Drone import Drone
from Model.DetectedMap import DMap
from random import randint
import pygame
import time

class Controller:
    def __init__(self, env, drone, dmap):
        self.__environment = env
        self.__drone = drone
        self.__dmap = dmap
        self.__start = False

    def start(self):
        # initialize the pygame module
        self.__environment.loadEnvironment("test2.map")
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("assets/logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((800, 400))
        screen.fill(utils.WHITE)
        screen.blit(self.__environment.image(), (0, 0))

        # define a variable to control the main loop
        running = True
        # main loop
        while running:
            # event handling, gets all event from the event queue

            # use this function instead of move
            # d.move(m)
            self._markDetectedWalls(self.__drone.xCoordinate, self.__drone.yCoordinate)
            if not self._moveDSF():
                running = False
                time.sleep(3)
            time.sleep(0.5)
            screen.blit(self.__dmap.image(self.__drone.xCoordinate, self.__drone.yCoordinate), (400, 0))
            pygame.display.flip()

        pygame.quit()

    def _moveDSF(self):
        x = self.__drone.xCoordinate
        y = self.__drone.yCoordinate

        possibleMoves = [
            [x - 1, y],
            [x, y - 1],
            [x + 1, y],
            [x, y + 1]
        ]

        for move in possibleMoves:
            [new_x, new_y] = move
            if self.__dmap.areCoordinatesValid(new_x, new_y) and not self.__dmap.areCoordinatesVisited(new_x, new_y):
                self.__dmap.appendHistory(self.__drone.xCoordinate, self.__drone.yCoordinate)
                self.__drone.xCoordinate = new_x
                self.__drone.yCoordinate = new_y
                self.__dmap.markAsVisited(new_x, new_y)
                return True

        # if no move is available/valid, go to a previous position to continue the DFS
        if len(self.__dmap.history) > 0:
            [prev_x, prev_y] = self.__dmap.getLastVisited()
            self.__drone.xCoordinate = prev_x
            self.__drone.yCoordinate = prev_y
            return True

        return False

    def _markDetectedWalls(self, x, y):
        walls = self.__environment.readUDMSensors(x, y)
        i = x - 1
        if walls[utils.UP] > 0:
            while (i >= 0) and (i >= x - walls[utils.UP]):
                self.__dmap.updateSurface(i, y, 0)
                i = i - 1
        if i >= 0:
            self.__dmap.updateSurface(i, y, 1)

        i = x + 1
        if walls[utils.DOWN] > 0:
            while (i < self.__dmap.rows) and (i <= x + walls[utils.DOWN]):
                self.__dmap.updateSurface(i, y, 0)
                i = i + 1
        if i < self.__dmap.rows:
            self.__dmap.updateSurface(i, y, 1)

        j = y + 1
        if walls[utils.LEFT] > 0:
            while (j < self.__dmap.columns) and (j <= y + walls[utils.LEFT]):
                self.__dmap.updateSurface(x, j, 0)
                j = j + 1
        if j < self.__dmap.columns:
            self.__dmap.updateSurface(x, j, 1)

        j = y - 1
        if walls[utils.RIGHT] > 0:
            while (j >= 0) and (j >= y - walls[utils.RIGHT]):
                self.__dmap.updateSurface(x, j, 0)
                j = j - 1
        if j >= 0   :
            self.__dmap.updateSurface(x, j, 1)

        return None

