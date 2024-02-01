import random
from solution import Solution
import copy

class Movements:
    def __init__(self, sol: Solution) -> None:
        self.sol = sol
        self.number_of_movements = 5

    
    def apply_movement(self, movement):
        solution = None
        if movement == 0:
            solution = self.swap_between_runs()
        elif movement == 1:
            solution = self.swap_in_run()
        elif movement == 2:
            solution = self.remove_insert()
        elif movement == 3:
            solution = self.remove_and_put_in_another_run()
        elif movement == 4:
            solution = self.insert_random_unused()

        solution.calculate_total_punctuation()
        solution.calculate_time()
        solution.calculate_total_complexity()

        return solution

    def swap_between_runs(self):
        copy_sol = copy.deepcopy(self.sol)  # Utilize deepcopy para criar uma cópia profunda

        index_1 = random.randint(0, len(self.sol.route) - 1)
        index_2 = random.randint(0, len(self.sol.route) - 1)
        
        while index_2 == index_1:
            index_2 = random.randint(0, len(self.sol.route) - 1)

        items_1 = self.sol.route[index_1]
        items_2 = self.sol.route[index_2]

        item_1_index = random.randint(1, len(items_1) - 2)
        item_2_index = random.randint(1, len(items_2) - 2)

        # Troca dos itens entre as rotas
        temp_item = copy.deepcopy(copy_sol.route[index_1][item_1_index])
        item_2 = copy.deepcopy(copy_sol.route[index_2][item_2_index])
        copy_sol.route[index_1][item_1_index] = item_2
        copy_sol.route[index_2][item_2_index] = temp_item

        #print(f"Trocando item: {temp_item['label']} com {item_2['label']}")


        return copy_sol


    def swap_in_run(self):
        copy_sol = copy.deepcopy(self.sol)

        index_1 = random.randint(0, len(self.sol.route) - 1)
        items_1 = copy_sol.route[index_1]

        item_1_index = random.randint(1, len(items_1) - 2)
        item_2_index = random.randint(1, len(items_1) - 2)
        
        item_1 = items_1[item_1_index]
        item_2 = items_1[item_2_index]

        copy_sol.route[index_1][item_1_index] = item_2
        copy_sol.route[index_1][item_2_index] = item_1

        return copy_sol

    def remove_insert(self):
        copy_sol = copy.deepcopy(self.sol)

        unused_index = random.randint(0, len(self.sol.unused) - 1)
        unused = copy_sol.unused[unused_index]

        index_1 = random.randint(1, len(copy_sol.route) - 2)
        items_1 = copy_sol.route[index_1]

        item_1_index = random.randint(1, len(items_1) - 2)
        item_1 = items_1[item_1_index]

        copy_sol.route[index_1][item_1_index] = unused
        copy_sol.unused.pop(unused_index)
        copy_sol.unused.append(item_1)

        return copy_sol
    
    def remove_and_put_in_another_run(self):
        copy_sol = copy.deepcopy(self.sol)
        greater_length = len(copy_sol.route[0])
        minor_length = len(copy_sol.route[0])

        current_minor_index = 0
        current_greater_index = 0

        for i in range(1, len(copy_sol.route) - 1):
            if len(copy_sol.route[i]) < minor_length:
                minor_length = len(copy_sol.route[i])
                current_minor_index = i
            
            if len(copy_sol.route[i]) > greater_length:
                greater_length = len(copy_sol.route[i])
                current_greater_index = i

        if greater_length > minor_length:
            greater_random_index = random.randint(1, len(copy_sol.route[current_greater_index]) - 2)
            greater_item = copy.deepcopy(copy_sol.route[current_greater_index][greater_random_index])
            copy_sol.route[current_minor_index].insert(len(copy_sol.route[current_minor_index]) - 2, greater_item)
            copy_sol.route[current_greater_index].pop(greater_random_index)
        
        return copy_sol
    
    def insert_random_unused(self):
        copy_sol = copy.deepcopy(self.sol)
        unused = copy.deepcopy(copy_sol.unused)

        random_index = random.randint(0, len(unused) - 1)
        minor_length = len(copy_sol.route[0])

        current_minor_index = 0

        for i in range(1, len(copy_sol.route) - 1):
            if len(copy_sol.route[i]) < minor_length:
                minor_length = len(copy_sol.route[i])
                current_minor_index = i

        copy_sol.route[current_minor_index].insert(len(copy_sol.route[current_minor_index]) - 2, unused[random_index])

        

        return copy_sol


