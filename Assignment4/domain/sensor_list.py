from utils import *
from domain.sensor import *
import random

class SensorList:
    def __init__(self, dmap):
        self.__sensorList = []
        self.__map = dmap

        self.place_sensors()

        self.distances_between_sensors = [[0 for _ in range(SENSOR_COUNT)] for _ in range(SENSOR_COUNT)]
        self.path_between_sensors = {}
        self._compute_distance_between_sensors()

        for sensor in self.__sensorList:
            sensor.detect_max_energy()
            sensor.compute_max_energy()

    def place_sensors(self):
        self.__sensorList.clear()

        for s in range(5):
            newX, newY = random.randint(0, 19), random.randint(0, 19)
            while self.__map.surface[newX][newY] != 0:
                newX, newY = random.randint(0, 19), random.randint(0, 19)

            self.__map.set_cell(newX, newY, 2)
            self.__sensorList.append(Sensor(newX, newY , self.__map))

    def _compute_distance_between_sensors(self):
        for i in range(len(self.__sensorList)):
            self.distances_between_sensors[i][i] = 0
            newX, newY = self.__sensorList[i].get_x(), self.__sensorList[i].get_y()
            for j in range(i + 1, len(self.__sensorList)):
                path = self.__map.searchAStar(newX, newY, self.__sensorList[j].get_x(), self.__sensorList[j].get_y())
                self.path_between_sensors[(i, j)] = path
                self.path_between_sensors[(j, i)] = path
                dist = INF if len(path) == 0 else len(path)
                self.distances_between_sensors[i][j] = self.distances_between_sensors[j][i] = dist

    def get_path_between_sensors(self, x, y):
        return self.path_between_sensors[(x, y)]

    def get_sensor_list(self):
        return self.__sensorList

    def get_distances_between_sensors(self):
        return self.distances_between_sensors