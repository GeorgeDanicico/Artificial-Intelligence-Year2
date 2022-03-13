import pickle
import pygame
from random import randint
import time
import utils
from Model.Drone import Drone
from Model.Map import Map
from Controller.Controller import Controller

class GUI:
    def __init__(self, drone, dmap):
        self.__controller = Controller(drone, dmap)

    def start(self):
        self.__controller.start()

