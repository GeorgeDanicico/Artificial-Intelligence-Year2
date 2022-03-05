import utils
import numpy as np
import pygame


class DMap:
    def __init__(self):
        self.__n = 20
        self.__m = 20
        self.__visited = []
        self.__visited_history = []
        self.__surface = np.zeros((self.__n, self.__m))
        for i in range(self.__n):
            for j in range(self.__m):
                self.__surface[i][j] = -1

    @property
    def rows(self):
        return self.__n

    @property
    def columns(self):
        return self.__m

    @property
    def visited(self):
        return self.__visited

    def markAsVisited(self, x, y):
        self.__visited.append([x, y])

    @property
    def history(self):
        return self.__visited_history

    def appendHistory(self, x, y):
        self.__visited_history.append([x, y])

    def updateSurface(self, x, y, value):
        self.__surface[x][y] = value

    def getLastVisited(self):
        return self.__visited_history.pop()

    def areCoordinatesVisited(self, x, y):
        return [x, y] in self.visited

    def areCoordinatesValid(self, x, y):
        return 0 <= x <= 19 and 0 <= y <= 19 and self.__surface[x][y] == 0

    def image(self, x, y):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        empty = pygame.Surface((20, 20))
        visited_cell = pygame.Surface((20, 20))
        visited_cell.fill(utils.RED)
        empty.fill(utils.WHITE)
        brick.fill(utils.BLACK)
        imagine.fill(utils.GRAYBLUE)

        for i in range(self.__n):
            for j in range(self.__m):
                if self.__surface[i][j] == 1:
                    imagine.blit(brick, (j * 20, i * 20))
                elif self.__surface[i][j] == 0 and [i, j] not in self.__visited:
                    imagine.blit(empty, (j * 20, i * 20))
                elif [i, j] in self.__visited:
                    imagine.blit(visited_cell, (j * 20, i * 20))

        drona = pygame.image.load("assets/drona.png")
        imagine.blit(drona, (y * 20, x * 20))

        return imagine