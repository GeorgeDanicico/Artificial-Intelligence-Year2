import utils
import numpy as np
import pygame
from random import random
import pickle


class Map:
    def __init__(self, n=20, m=20):
        self.__n = n
        self.__m = m
        self.surface = np.zeros((self.__n, self.__m))

    def randomMap(self, fill=0.2):
        for i in range(self.__n):
            for j in range(self.__m):
                if random() <= fill:
                    self.surface[i][j] = 1

    @property
    def rows(self):
        return self.__n

    @property
    def columns(self):
        return self.__m

    def areCoordinatesValid(self, x, y):
        return 0 <= x <= 19 and 0 <= y <= 19 and self.surface[x][y] == 0

    def __str__(self):
        string=""
        for i in range(self.__n):
            for j in range(self.__m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def saveMap(self, numFile="test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def image(self, colour=utils.BLUE, background=utils.WHITE):
        imagine = pygame.Surface((400, 400))
        brick = pygame.Surface((20, 20))
        brick.fill(utils.BLUE)
        imagine.fill(utils.WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if self.surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))

        return imagine