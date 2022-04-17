from pygame.locals import *
import pygame, time
from utils import *
from domain import *
import numpy as np


def initPyGame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with AE")

    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def closePyGame():
    # closes the pygame
    running = True
    # loop for events
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    pygame.quit()


def movingDrone(currentMap, sensor_list, path, speed=1, markSeen=True):
    # animation of a drone on a path

    screen = initPyGame((currentMap.n * 20, currentMap.m * 20))
    visited = np.zeros((20, 20))
    drona = pygame.image.load("drona.png")
    sensor = pygame.image.load("sensor.jpg")
    screen.blit(image(currentMap), (0, 0))

    for i in range(len(path)):
        screen.blit(image(currentMap), (0, 0))

        for sensors in sensor_list.get_sensor_list():
            # brick = pygame.Surface((20, 20))
            # brick.fill(GREEN)
            screen.blit(sensor, (sensors.get_y() * 20, sensors.get_x() * 20))

        for ii in range(20):
            for jj in range(20):
                if visited[ii][jj] == 1:
                    brick = pygame.Surface((20, 20))
                    brick.fill(GREEN)
                    screen.blit(brick, (jj * 20, ii * 20))
        visited[path[i][0]][path[i][1]] = 1
        screen.blit(drona, (path[i][1] * 20, path[i][0] * 20))
        pygame.display.flip()
        time.sleep(0.5 * speed)
    closePyGame()


def image(currentMap, colour=BLUE, background=WHITE):
    # creates the image of a map

    imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
    brick = pygame.Surface((20, 20))
    brick.fill(colour)
    imagine.fill(background)
    for i in range(currentMap.n):
        for j in range(currentMap.m):
            if currentMap.surface[i][j] == 1:
                imagine.blit(brick, (j * 20, i * 20))

    return imagine        