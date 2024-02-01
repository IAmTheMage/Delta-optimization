from utils import Utils

class Solution:
    def __init__(self, route, complexity, time, unused, complexity_weight, time_weight, punctuation_weight) -> None:
        self.route = route
        self.complexity = complexity
        self.time = time
        self.total_complexity = 0.0
        self.utils: Utils = None
        for comp in self.complexity:
            self.total_complexity += comp

        self.unused = unused

        self.complexity_weight = complexity_weight
        self.time_weight = time_weight
        self.punctuation_weight = punctuation_weight

        self.total_punctuation = 0
        for route_item in self.route:
            for item in route_item:
                if "punctuation" in item:
                    self.total_punctuation += item["punctuation"]

    def __str__(self) -> str:
        
        ret = "Solution\n"
        ret += "Time: " + str(self.time) + "\n"
        ret += "Complexity: " + str(self.total_complexity) + "\n"
        ret += "Total Punctuation: " + str(self.total_punctuation) + "\n"
        ret += "Route: \n"
        index = 0
        for route_item in self.route:
            ret += "["
            current_index = 0
            for item in route_item:
                ret += item["label"]
                if current_index < len(route_item) - 1:
                    ret += ','
                current_index += 1
            ret += "]"
            if index < len(self.route) - 1:
                ret += ", "
            index += 1

        return ret
    
    def __gt__(self, another_solution):
        _punctuation = self.total_complexity * self.complexity_weight
        _punctuation += self.time * self.time_weight

        _punctuation -= self.total_punctuation * self.punctuation_weight

        _another_punctuation = another_solution.total_complexity * another_solution.complexity_weight
        _another_punctuation += another_solution.time * another_solution.time_weight

        _another_punctuation -= another_solution.total_punctuation * another_solution.punctuation_weight

        return _punctuation < _another_punctuation
    
    def get_eval(self):
        _punctuation = self.total_complexity * self.complexity_weight
        _punctuation += self.time * self.time_weight

        _punctuation -= self.total_punctuation * self.punctuation_weight
        return _punctuation
    
    def copy(self):
        return Solution(
            self.route,
            self.complexity,
            self.time,
            self.unused,
            self.complexity_weight,
            self.time_weight,
            self.punctuation_weight
        )
    
    def print_sol_labels(self):
        ret = ""
        index = 0
        for route_item in self.route:
            ret += "["
            current_index = 0
            for item in route_item:
                ret += item["label"]
                if current_index < len(route_item) - 1:
                    ret += ','
                current_index += 1
            ret += "]"
            if index < len(self.route) - 1:
                ret += ", "
            index += 1

        print(ret)


    def calculate_time(self):
        sum = 0.0
        for route_items in self.route:
            for i in range(1, len(route_items)):
                item_previous = route_items[i-1]
                item = route_items[i]

                distance_between_missions = self.utils.get_real_distance(item_previous, item)
                time_needed = distance_between_missions / 220
                if "time_needed" in item:
                    time_needed += item["time_needed"]
                sum += time_needed
        self.time = sum

    def calculate_total_punctuation(self):
        punct = 0
        for i in self.route:
            for j in i:
                if "punctuation" in j:
                    punct += j["punctuation"]

        self.total_punctuation = punct

    
    def calculate_total_complexity(self):
        self.total_complexity = 0
        for item in self.route:
            self.total_complexity += self.utils.calculate_current_complexity(item)
        

    def calculate_insertion_time(self, point, route_index, position_index):
        if not "time_needed" in point:
            raise "O ponto precisa ser uma missão"
        
        else:
            route_item = self.route[route_index]

            if len(route_item) - 1 == position_index or position_index == 0:
                raise "O ponto não pode ser o ultimo nem o primeiro da rota"
            
            temp_distance = self.utils.get_real_distance(route_item[position_index-1], route_item[position_index+1])
            time_to_remove = temp_distance / 220
            #self.time -= time_to_remove

            temp_distance = self.utils.get_real_distance(route_item[position_index], route_item[position_index-1])
            time_to_add = temp_distance / 220

            temp_distance = self.utils.get_real_distance(route_item[position_index], route_item[position_index+1])
            time_to_add += temp_distance / 220

            time_to_add += point["time_needed"]

            #self.route[route_index].insert(position_index, point)
            #self.time += time_to_add
            return time_to_add - time_to_remove

    

    def feasible(self) -> bool:
        self.calculate_total_punctuation()
        self.calculate_time()
        self.calculate_total_complexity()

        return self.time <= self.utils.configuration["max_time"] and self.total_complexity <= self.utils.configuration["max_complexity"] * self.utils.configuration["runs"]


    def calculate_unused(self):
        labels = []

        for i in self.route:
            for j in i:
                labels.append(j["label"])

        unused = []

        for j in self.utils.configuration["positions"]:
            valid = True
            for k in labels:
                if k == j["label"]:
                    valid = False

            if valid == True:
                unused.append(j)

        self.unused = unused