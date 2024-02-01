import math

class Utils:
    def __init__(self, configuration) -> None:
        self.configuration = configuration

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
    
    def calculate_current_complexity(self, route_items):
        index = 0
        current_complexity = 0.0
        for item in route_items:
            if "factor" in item:
                current_complexity += item["factor"] * self.configuration["weights"]["complexity"] * (1+self.configuration["complexity_scale"]*index)
        
        return current_complexity