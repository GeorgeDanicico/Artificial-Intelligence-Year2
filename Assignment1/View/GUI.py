import pickle
import pygame
from random import randint
import time
import utils
from Model.Environment import Environment
from Model.Drone import Drone
from Model.DetectedMap import DMap
from Controller.Controller import Controller

class GUI:
    def __init__(self, env, drone, dmap):
        self.__controller = Controller(env, drone, dmap)

    def start(self):
        self.__controller.start()

