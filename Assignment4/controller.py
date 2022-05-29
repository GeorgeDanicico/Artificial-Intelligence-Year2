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

        self.sensors = SensorList(self.map)
        self.pheromones = [[1.0 for _ in range(SENSOR_COUNT)] for _ in range(SENSOR_COUNT)]
        self.distances = self.sensors.get_distances_between_sensors()

    def move_ants(self, ants, alpha, beta, q0):
        """
        Move all the ants
        :param ants:  ants array
        :param alpha:
        :param beta:
        :param q0: the probability to pick the best solution
        :return: the ants that could travel to all the sensors.
        """
        all_ants = [True for _ in ants]
        for i in range(len(ants)):
            ant = ants[i]
            for j in range(ANT_MOVES - 1):
                # if the ant can't perform a new move, we kill it
                possible_move = ant.next_move(self.distances, self.pheromones, q0, alpha, beta)
                if not possible_move:
                    all_ants[i] = False
                    break

        alive_ants = []
        for i in range(len(ants)):
            if all_ants[i]:
                ants[i].compute_fitness(self.distances)
                alive_ants.append(ants[i])
        return alive_ants

    def choose_best_ant(self, ants):
        """
        choose the ant with the best fitness
        :param ants: the ants that travel to all the sensors.
        :return: the best ant
        """
        best_ant = None
        best_fitness = INF

        for ant in ants:
            if best_fitness > ant.get_fitness():
                best_fitness = ant.get_fitness()
                best_ant = ant
        return best_ant

    def epoch(self, ants_count, alpha, beta, q0, rho):
        ants = [Ant(ANT_MOVES, BATTERY_STATUS) for _ in range(ants_count)]

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

    def charge_sensors(self, battery_status, available_sensors):
        """
        after traversing through all the sensors,
        we distribute the remaining battery in order to get the maximum surveyed cells
        :param battery_status: the remaining energy after a traversal
        :param available_sensors:
        :return:
        """
        print("Battery left after shortest path: ", battery_status)
        sensors = []
        for i in range(len(self.sensors.get_sensor_list())):
            if i in available_sensors:
                sensors.append(self.sensors.get_sensor_list()[i])

        energy = [0 for _ in sensors]
        if battery_status <= 0:
            return energy

        sensors.sort(key=lambda s: (s.get_accessible_positions()[-1] / s.get_max_energy()))
        i = 0
        while i < len(sensors) and battery_status > 0:
            current_sensor_max_energy = sensors[i].get_max_energy()
            if battery_status > current_sensor_max_energy:
                battery_status -= current_sensor_max_energy
                energy[i] = current_sensor_max_energy
            else:
                energy[i] = battery_status
                battery_status = 0
            i += 1
        return energy

    def _iteration(self, best_choice):

        current_sol = self.epoch(30, alpha=1.9, beta=0.9, q0=0.5, rho=0.05)
        if current_sol is None:
            return best_choice

        length = len(current_sol.get_path())
        if best_choice is None or length > len(best_choice.get_path()) \
                or (length == len(best_choice.get_path()) and current_sol.get_fitness() < best_choice.get_fitness()):
            return current_sol  # new best solution
        return best_choice

    def generate_path(self, drone, sensors_path):
        [x, y] = drone.get_coordinates()
        sensor_list = self.sensors.get_sensor_list()
        current_sensor = sensor_list[sensors_path[0]]
        full_path = self.map.searchAStar(x, y, current_sensor.get_x(), current_sensor.get_y())[::-1]

        (x, y) = current_sensor.get_coords()

        for i in range(1, SENSOR_COUNT):
            current_sensor = sensor_list[sensors_path[i]]
            full_path += self.map.searchAStar(x, y, current_sensor.get_x(), current_sensor.get_y())[::-1]
            (x, y) = current_sensor.get_coords()
        return full_path

    def run(self):
        best_choice = None  # will be the one with the largest number of visible positions
        for _ in range(1000):
            best_choice = self._iteration(best_choice)

        energy = self.charge_sensors(BATTERY_STATUS - best_choice.get_fitness(), best_choice.get_path())
        print('Energy distributed: ', energy)
        print('Best path: ', best_choice.get_path())

        return self.generate_path(self.drone, best_choice.get_path())

    def view_map(self):
        gui.movingDrone(self.map, self.sensors, self.run())

    def get_map(self):
        return self.map

    def get_surface(self):
        return self.map.surface

    def get_drone_position(self):
        return self.drone.get_coordinates()