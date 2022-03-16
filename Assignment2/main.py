import pickle
from Model.Drone import Drone
from Model.Map import Map
from random import randint
from View.GUI import GUI


def main():

    x = randint(1, 19)
    y = randint(1, 19)

    drone = Drone(x, y)

    map = Map()

    gui = GUI(drone, map)
    gui.start()


if __name__ == "__main__":
    # call the main function
    main()
