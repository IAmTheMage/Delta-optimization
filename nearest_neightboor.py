import json
from PIL import Image, ImageDraw
import random
import math
from solution import Solution
from utils import Utils


class Constructive:
    def __init__(self, path) -> None:
        with open(path) as file:
            # Carregue o conteúdo do arquivo em uma variável
            self.configuration = json.load(file)

        self.utils = Utils(self.configuration)

        self.mat_sizes = {
            "L": 2000,
            "W": 1200
        }

        self.img_size = {
            "L": 1280,
            "W": 720
        }

        self.img_output_size = {
            "L": 2466,
            "W": 1444
        }

        self.robot_velocity_mean_mm = 220

        self.current_position = self.configuration["safe_areas"][0]

        WIDTH_CONSTRAINT = self.img_output_size["L"] / self.img_size["L"]
        HEIGHT_CONSTRAINT = self.img_output_size["W"] / self.img_size["W"]

        print(WIDTH_CONSTRAINT)
        print(HEIGHT_CONSTRAINT)

        self.copy_missions = list(self.configuration["positions"])




    def sort_key(self, item):
        x_dist = (item["x"] - self.current_position["x"])**2
        y_dist = (item["y"] - self.current_position["y"])**2
        return math.sqrt((x_dist + y_dist))

    def get_distance(self, item_previous, item):
        x_dist = (item["x"] - item_previous["x"])**2
        y_dist = (item["y"] - item_previous["y"])**2
        return math.sqrt(x_dist + y_dist)

    def get_real_distance(self, item_previous, item):
        x_dist = (item["x"] - item_previous["x"])**2
        y_dist = (item["y"] - item_previous["y"])**2
        distance_in_image = (x_dist + y_dist)**0.5  # Distância na imagem

        # Proporções entre a imagem e a mesa
        mesa_width = self.mat_sizes["L"]  # largura da mesa em metros
        mesa_height = self.mat_sizes["W"]  # altura da mesa em metros

        scale_width = self.img_size["L"]
        scale_height = self.img_size["W"]

        # Converter distância da imagem para a mesa usando as proporções
        scale_mesa_width = mesa_width / scale_width
        scale_mesa_height = mesa_height / scale_height

        # Convertendo a distância da imagem para a mesa real
        distance_in_meters = distance_in_image * min(scale_mesa_width, scale_mesa_height)

        return distance_in_meters

    def sum_times(self, route_items):
        sum = 0.0
        if len(route_items) == 1:
            return sum
        if len(route_items) > 1:
            sum += route_items[1]["time_needed"]
        for i in range(1, len(route_items)):
            item_previous = route_items[i-1]
            item = route_items[i]

            distance_between_missions = self.get_real_distance(item_previous, item)
            time_needed = distance_between_missions / self.robot_velocity_mean_mm
            if "time_needed" in item:
                time_needed += item["time_needed"]
            sum += time_needed
        return sum


    def find_to_poppy(self, name):
        index = 0
        for item in self.copy_missions:
            if name == item["label"]:
                return index
            index += 1
            
        return -1

    def find_nearest_safe_area(self):
        distance_1 = self.get_distance(self.configuration["safe_areas"][0], self.current_position)
        distance_2 = self.get_distance(self.configuration["safe_areas"][1], self.current_position)

        #print(f'Distance from: {self.configuration["safe_areas"][0]["x"]} {self.configuration["safe_areas"][0]["y"]} and {self.current_position["x"]} {self.current_position["y"]} is {distance_1}')
        #print(f'Distance from: {self.configuration["safe_areas"][1]["x"]} {self.configuration["safe_areas"][1]["y"]} and {self.current_position["x"]} {self.current_position["y"]} is {distance_2}')

        if distance_1 < distance_2:
            return 0
        return 1

    def calculate_current_complexity(self, route_items):
        index = 0
        current_complexity = 0.0
        for item in route_items:
            if "factor" in item:
                current_complexity += item["factor"] * self.configuration["weights"]["complexity"] * (1+self.configuration["complexity_scale"]*index)
        
        return current_complexity
    
    def calculate_item_complexity(self, item, index):
        current_complexity = item["factor"] * self.configuration["weights"]["complexity"] * (1+self.configuration["complexity_scale"]*index)
        return current_complexity
    

    def calculate_item_time(self, item):
        sum = 0
        if "time_needed" in item:
            sum += item["time_needed"]  

        distance_between_missions = self.get_real_distance(self.current_position, item)
        sum += distance_between_missions / self.robot_velocity_mean_mm
        return sum


    def nearest_neightboor(self):
        route = []
        complexity = []
        total_time = 0.0
        print("Starting constructing solution by nearest neightboor")
        for i in range(self.configuration["runs"]):
            route_item = []
            current_time = self.configuration["max_time"] / self.configuration["runs"]
            if i == 0:
                route_item.append(self.configuration["safe_areas"][0])

            else:
                route_item.append(route[i - 1][len(route[i - 1])-1])
            
            index = 0
            while True:
                times = self.sum_times(route_item)
                sorted_neightboors = sorted(self.copy_missions, key=self.sort_key)
                max_comp = self.calculate_current_complexity(route_item) + self.calculate_item_complexity(sorted_neightboors[0], index)

                if times + self.calculate_item_time(sorted_neightboors[0]) > self.configuration["max_time"] / self.configuration["runs"] or len(self.copy_missions) == 1 or max_comp >= self.configuration["max_complexity"]:
                    complexity.append(max_comp)
                    break
                

                if len(sorted_neightboors) == 0:
                    break

                route_item.append(sorted_neightboors[0])
                self.current_position = sorted_neightboors[0]
                finded_index = self.find_to_poppy(sorted_neightboors[0]["label"])
                self.copy_missions.pop(finded_index)
                index += 1

            route_item.append(self.configuration["safe_areas"][self.find_nearest_safe_area()])
            
            self.current_position = self.configuration["safe_areas"][self.find_nearest_safe_area()]
            route.append(route_item)

        
        for items in route:
            total_time += self.sum_times(items)

        
        solution = Solution(route, complexity, total_time, self.copy_missions, self.configuration["simulated_anealing_configuration"]["weights"]["complexity"], 
                        self.configuration["simulated_anealing_configuration"]["weights"]["time"], self.configuration["simulated_anealing_configuration"]["weights"]["punctuation"])
        solution.utils = self.utils
        return solution
    