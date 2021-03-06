# -*- coding: utf-8 -*-


# imports
import matplotlib.pyplot as pl
from gui import *
from controller import *
from repository import *
from domain import *
import time

# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls

class UI:
    def __init__(self, controller):
        self.__controller = controller
        self.__path = None
        self.__statistics_info = None

    @staticmethod
    def print_menu():
        print('Choose one of the below options:\n'
              '\t1. create random map\n'
              '\t2. load a map\n'
              '\t3. save a map\n'
              '\t4. visualize the map\n'
              '\t5. run\n'
              '\t0. exit')

    @staticmethod
    def print_ea_options():
        print('Choose one of the below options:\n'
              '\t1. Parameters Setup\n'
              '\t2. Run the solver\n'
              '\t3. Visualise the statistics\n'
              '\t4. View the drone moving on a path\n'
              '\t0. Go back')

    @staticmethod
    def print_parameters_setup():
        print('Choose one of the below options:\n'
              '\t1. Set the population size\n'
              '\t2. Set the individual size\n'
              '\t3. Set the number of iterations\n'
              '\t4. Set the number of runs\n'
              '\t5. Set mutate probability\n'
              '\t6. Set crossover probability\n'
              '\t0. Go back')

    def set_population_size(self):
        new_value = int(input('Enter population size: '))
        self.__controller.set_population_size(new_value)
        print('Population size has been updated.\n')

    def set_individual_size(self):
        new_value = int(input('Enter individual size: '))
        self.__controller.set_individual_size(new_value)
        print('Population size has been updated.\n')

    def set_mutate_probability(self):
        new_value = int(input('Enter mutate probability: '))
        self.__controller.set_mutate_probability(new_value)
        print('Mutate probability has been updated.\n')

    def set_crossover_probability(self):
        new_value = int(input('Enter crossover probability: '))
        self.__controller.set_crossover_probability(new_value)
        print('Crossover probability has been updated.\n')

    def set_iterations(self):
        new_value = int(input('Enter iterations: '))
        self.__controller.set_iterations(new_value)
        print('Number of iterations has been updated.\n')

    def set_runs(self):
        new_value = int(input('Enter number of runs: '))
        self.__controller.set_runs(new_value)
        print('Number of runs has been updated.\n')

    def load_map(self):
        file_name = input("The file name: ")
        self.__controller.load_map(file_name)
        print("File loaded successfully \n")

    def save_map(self):
        file_name = input("The file name: ")
        self.__controller.save_map(file_name)
        print("File saved successfully \n")

    def view_statistics(self):
        indices = [index for index in range(len(self.__statistics_info))]
        average_of_fitnesses = [stat[0] for stat in self.__statistics_info]
        deviation = [stat[1] for stat in self.__statistics_info]

        pl.plot(indices, average_of_fitnesses, label="Average Fitness")
        pl.plot(indices, deviation, label="Standard Deviation")
        pl.show()

    def setup_parameters(self):
        finished = False
        while not finished:
            self.print_parameters_setup()
            choice = input("Your choice is: ")
            if choice == '0':
                finished = True
                print('Back...\n')
            elif choice == '1':
                self.set_population_size()
            elif choice == '2':
                self.set_individual_size()
            elif choice == '3':
                self.set_iterations()
            elif choice == '4':
                self.set_runs()
            elif choice == '5':
                self.set_mutate_probability()
            elif choice == '6':
                self.set_crossover_probability()
            else:
                print("Wrong choice!\n\n")

    def move_drone(self):
        print('The path is: ', self.__path)
        movingDrone(self.__controller.get_map(), self.__path)

    def run_solver(self):
        start = time.time()
        self.__path, self.__statistics_info = self.__controller.solver()
        end = time.time()

        print("Execution Time: ", end - start)

    def run(self):
        finished = False
        while not finished:
            self.print_ea_options()
            choice = input("Your choice is: ")
            if choice == '0':
                finished = True
                print('Back...\n')
            elif choice == '1':
                self.setup_parameters()
            elif choice == '2':
                self.run_solver()
            elif choice == '3':
                self.view_statistics()
            elif choice == '4':
                self.move_drone()
            else:
                print("Wrong choice!\n\n")

    def start(self):
        finished = False
        while not finished:
            self.print_menu()
            choice = input("Your choice is: ")
            if choice == '0':
                finished = True
                print('Goodbye!')
            elif choice == '1':
                self.__controller.generate_random_map()
            elif choice == '2':
                self.load_map()
            elif choice == '3':
                self.save_map()
            elif choice == '4':
                self.__controller.view_map()
            elif choice == '5':
                self.run()
            else:
                print("Wrong choice!\n\n")