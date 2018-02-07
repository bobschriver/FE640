import math
import numpy as np

class Cost():
    def configure(self):
        return

class SSE(Cost):
    def configure(self, target):
        self.target = target
        
    def calculate(self, solution):
        sse = 0
        for harvest in solution.harvests:
            sse += math.pow((self.target - harvest.volume), 2)
        
        return sse

class MinMax(Cost):
    def calculate(self, solution):
        harvest_volumes = [harvest.volume for harvest in solution.harvests]
        return max(harvest_volumes)
       
class Variance(Cost):
    def calculate(self, solution):
        harvest_volumes = [harvest.volume for harvest in solution.harvests]
        return np.var(harvest_volumes)