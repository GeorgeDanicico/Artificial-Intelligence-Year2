import pickle
from Model.Environment import Environment
from Model.Drone import Drone
from Model.DetectedMap import DMap
from random import randint
from View.GUI import GUI


def main():
    env = Environment()
    env.loadEnvironment("test2.map")

    x = randint(1, 19)
    y = randint(1, 19)
    drone = Drone(x, y)

    dmap = DMap()
    dmap.markAsVisited(x, y)

    gui = GUI(env, drone, dmap)
    gui.start()


if __name__ == "__main__":
    # call the main function
    main()
