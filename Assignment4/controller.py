from domain.map import Map
from domain.drone import Drone
from domain.ant import Ant
from domain.sensor_list import SensorList
import random
from utils import *
import gui

class Controller:
    def __init__(self, map, drone):
        self.map = map
        self.drone = drone

        self.__sensors = SensorList(self.map)
        self.pheromones = [[1.0 for _ in range(SENSOR_COUNT * 4)] for _ in range(SENSOR_COUNT * 4)]
        self.distances = self.__sensors.getDistBetweenSensors()

    def move_ants(self, ants, alpha, beta, q0):
        all_ants = [True for _ in ants]
        for i in range(len(ants)):
            ant = ants[i]
            for step in range(ANT_MOVES - 1):
                found = ant.next_move(self.distances, self.pheromones, q0, alpha, beta)
                if not found:
                    all_ants[i] = False
                    break

        alive_ants = []
        for i in range(len(ants)):
            if all_ants[i]:
                ants[i].compute_fitness(self.distances)
                alive_ants.append(ants[i])
        return alive_ants

    def choose_best_ant(self, ants):
        best_ant = None
        best_fitness = INF

        for ant in ants:
            if best_fitness > ant.get_fitness():
                best_fitness = ant.get_fitness()
                best_ant = ant
        return best_ant

    def simulate_epoch(self, ants_count, alpha, beta, q0, rho):
        ants = [Ant(ANT_MOVES, 100) for _ in range(ants_count)]

        ants = self.move_ants(ants, alpha, beta, q0)

        for i in range(SENSOR_COUNT):
            for j in range(SENSOR_COUNT):
                self.pheromones[i][j] = (1 - rho) * self.pheromones[i][j]

        if not ants:
            return None

        new_pheromones = [1.0 / ant.get_fitness() for ant in ants]
        for i in range(len(ants)):
            current = ants[i].get_path()
            for j in range(len(current)-1):
                current_sensor = current[j]
                next_sensor = current[j+1]
                self.pheromones[current_sensor][next_sensor] += new_pheromones[i]

        return self.choose_best_ant(ants)

    def charge_sensors(self, remaining_battery, available_sensors):
        sensors = []
        for i in range(len(self.__sensors.get_sensor_list())):
            if i in available_sensors:
                sensors.append(self.__sensors.get_sensor_list()[i])

        energy = [0 for _ in sensors]
        if remaining_battery <= 0:
            return energy

        sensors.sort(key=lambda s: (s.get_accessible_positions()[-1] / s.get_max_energy()))
        i = 0
        while i < len(sensors) and remaining_battery > 0:
            currentSensorMaxEnergy = sensors[i].get_max_energy()
            if remaining_battery > currentSensorMaxEnergy:
                remaining_battery -= currentSensorMaxEnergy
                energy[i] = currentSensorMaxEnergy
            else:
                energy[i] = remaining_battery
                remaining_battery = 0
            i += 1
        return energy

    def __updateBestSolution(self, bestSolution):
        currentSolution = self.simulate_epoch(30, alpha=1.9, beta=0.9, q0=0.5, rho=0.05)
        if currentSolution is None:
            return bestSolution

        currentSolutionPathLength = len(currentSolution.get_path())
        if bestSolution is None or currentSolutionPathLength > len(bestSolution.get_path()) \
                or (currentSolutionPathLength == len(bestSolution.get_path()) and currentSolution.get_fitness() < bestSolution.get_fitness()):
            return currentSolution  # new best solution
        return bestSolution

    def generate_path(self, drone, sensors_path):
        [x, y] = drone.get_coordinates()
        sensor_list = self.__sensors.get_sensor_list()
        current_sensor = sensor_list[sensors_path[0]]
        full_path = self.map.searchAStar(x, y, current_sensor.get_x(), current_sensor.get_y())[::-1]

        (x, y) = current_sensor.get_coords()

        for i in range(1, SENSOR_COUNT):
            current_sensor = sensor_list[sensors_path[i]]
            full_path += self.map.searchAStar(x, y, current_sensor.get_x(), current_sensor.get_y())[::-1]
            (x, y) = current_sensor.get_coords()
        return full_path

    def run(self):
        bestSolution = None  # will be the one with the largest number of visible positions
        for _ in range(1000):
            bestSolution = self.__updateBestSolution(bestSolution)

        energyLevels = self.charge_sensors(100 - bestSolution.get_fitness(), bestSolution.get_path())
        print('Energy distributed: ', energyLevels)
        print('Best path: ', bestSolution.get_path())

        return self.generate_path(self.drone, bestSolution.get_path())

    def view_map(self):
        gui.movingDrone(self.map, self.__sensors, self.run())

    def get_map(self):
        return self.map

    def get_surface(self):
        return self.map.surface

    def get_drone_position(self):
        return self.drone.get_coordinates()