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
    
    def __str__(self):
        return str(self.harvests)
    
    def __repr__(self):
        return str(self)
        
    def __eq__(self, other):
        for harvest, other_harvest in zip(self.harvests, other.harvests):
            if harvest != other_harvest:
                return False
                
        return True
        
    def __ne__(self, other):
        return not self.__eq__(other)
        