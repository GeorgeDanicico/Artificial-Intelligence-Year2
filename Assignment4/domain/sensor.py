from utils import *

class Sensor:
    def __init__(self, x, y, dmap):
        self.x = x
        self.y = y
        self.__accPositions = [0 for _ in range(6)]
        self.map = dmap
        self.max_energy = 0

    def detect_max_energy(self):
        blocked = [False for _ in range(4)]

        # energy value between 1-5
        for i in range(1, 6):
            self.__accPositions[i] = self.__accPositions[i-1]
            for d in range(4):
                if not blocked[d]:
                    newX = self.x + DIRECTIONS[d][0] * i
                    newY = self.y + DIRECTIONS[d][1] * i
                    if self.map.valid_neighbour(newX, newY):
                        self.__accPositions[i] += 1
                    else:
                        blocked[d] = True

    def compute_max_energy(self):
        for energy in range(5):
            if self.__accPositions[energy] == self.__accPositions[energy + 1]:
                self.max_energy = energy
                return
        self.max_energy = 5

    def get_max_energy(self):
        return self.max_energy

    def get_accessible_positions(self):
        return self.__accPositions

    def get_coords(self):
        coord = (self.x, self.y)
        return coord

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
