import pygame

from random import random, randint

from controller import Controller
from domain.drone import Drone
from domain.map import Map
import gui

WHITE = (255, 255, 255)

if __name__ == "__main__":

    # create map
    m = Map(20, 20)
    [x, y] = m.generate_drone_initial_position()

    d = Drone(x, y)
    controller = Controller(m, d)

    controller.view_map()
