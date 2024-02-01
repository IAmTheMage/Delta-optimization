import random
from movements import Movements
import math
from solution import Solution
import copy

class SA:
    def __init__(self, start_temperature=100, finishing_temperature=0.05, iterations_per_temperature=10, gamma=0.1, type="linear", language="english", steps = 5) -> None:
        self.start_temperature = start_temperature
        self.iterations_per_temperature = iterations_per_temperature
        self.gamma = gamma
        self.type = type
        self.language = language
        self.finishing_temperature = finishing_temperature
        self.current_season = "Masterpiece/2023 - 2024"
        self.steps = steps

    def execute(self, initial_solution):
        start_point = copy.deepcopy(initial_solution)
        global_best = copy.deepcopy(initial_solution)
        for step in range(self.steps):
            print(f"Starting execute Simulated Anealing, step {step}")
            current_temperature = self.start_temperature
            current_best = start_point
            
            while current_temperature > self.finishing_temperature:
                #print(f"Temperature: {current_temperature}")
                for i in range(10):
                    movement = Movements(current_best)
                    random_mvm = random.randint(0, movement.number_of_movements - 1)
                    #print(f"Aplicando movimento {random_mvm}")
                    new_solution = movement.apply_movement(random_mvm)

                    if new_solution > global_best and new_solution.feasible():
                        global_best = new_solution

                    else:
                        diff = new_solution.get_eval() - global_best.get_eval()
                        metropolis = math.exp(-diff / current_temperature)
                        if metropolis >= random.random():
                            current_best = new_solution

                current_temperature *= (1-self.gamma)

            test = self.insert_unused_in_random_positions(global_best, global_best.unused)
            global_best = copy.deepcopy(test)
            start_point = copy.deepcopy(test)

        ''' global_best.calculate_total_punctuation()

            start_point = self.insert_unused_in_random_positions(global_best, global_best.unused)
            global_best = copy.deepcopy(start_point)'''
        
        return global_best
        
    def insert_unused_in_random_positions(self, start_point: Solution, _unused):
        copy_solution = copy.deepcopy(start_point)
        copy_solution.calculate_time()
            
        random_route_index = 0
        random_point = 0
        copy_solution.calculate_unused()
        unused = copy.deepcopy(copy_solution.unused)
        for i in range(len(unused)):
            
            random_route_index = random.randint(0, len(copy_solution.route) - 1)
            random_route = copy_solution.route[random_route_index]
            random_point = random.randint(1, len(random_route) - 2)

            time_i = copy_solution.calculate_insertion_time(unused[i], random_route_index,
                                                            random_point)

            if time_i + copy_solution.time < copy_solution.utils.configuration["max_time"]:
                copy_solution.route[random_route_index].insert(random_point, unused[i])

                copy_solution.calculate_time()
                copy_solution.calculate_unused()
                break
        
        copy_solution.calculate_total_punctuation()
        return copy_solution 


    def __str__(self) -> str:
        data = ""
        if self.language == 'english':
            data = "Simulated Anealing for FLL competitions\n"
            data += "Start Temperature: " + str(self.start_temperature) + "\n"
            data += "Finishing Temperature: " + str(self.finishing_temperature) + "\n"
            data += "Iterations per Temperature: " + str(self.iterations_per_temperature) + "\n"
            data += "Gamma: " + str(self.gamma) + "\n"
            data += "Type: " + str(self.type) + "\n"
            data += "Season: " + str(self.current_season)
            return data
        else:
            data = "Simulated Anealing para as competições da FLL\n"
            data += "Temperatura Inicial: " + str(self.start_temperature) + "\n"
            data += "Temperatura Final: " + str(self.finishing_temperature) + "\n"
            data += "Iterações por Temperatura: " + str(self.iterations_per_temperature) + "\n"
            data += "Gama: " + str(self.gamma) + "\n"
            data += "Tipo: " + str(self.type) + "\n"
            data += "Temporada: " + str(self.current_season)
            return data
