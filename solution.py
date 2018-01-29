import random
import sys
import copy

from harvest import Harvest

class Solution:
    def __init__(self, num_harvests=3):
        self.num_harvests = num_harvests
        self.harvests = [Harvest(i) for i in range(num_harvests)]
        self.cost = sys.maxsize
   
    def from_plots(self, plots):
        for plot in plots:
            random.choice(self.harvests).add_plot(plot)
    
    def from_solution(self, solution):
        for i, harvest in enumerate(solution.harvests):
            self.harvests[i] = Harvest(i)
            self.harvests[i].from_harvest(harvest)
    
    def generate_neighbor(self):
        neighbor_solution = Solution(self.num_harvests)
        neighbor_solution.from_solution(self)
        
        first_harvest = random.choice(neighbor_solution.harvests)
        while(len(first_harvest.plots) == 0):
            first_harvest = random.choice(neighbor_solution.harvests)
    
        swap_plot = first_harvest.remove_random_plot()
    
        second_harvest = random.choice(neighbor_solution.harvests)
        while(second_harvest == first_harvest):
            second_harvest = random.choice(neighbor_solution.harvests)
        
        second_harvest.add_plot(swap_plot)
        return neighbor_solution
    
    def __str__(self):
        return str(self.harvests)
    
    def __repr__(self):
        return str(self)