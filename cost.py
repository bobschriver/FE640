import math

class SSE():
    def __init__(self, target):
        self.target = target
        
    def calculate(self, solution):
        sse = 0
        for harvest in solution.harvests:
            sse += math.pow((self.target - harvest.volume), 2)
        
        return sse

class MinMax():
    def calculate(self, solution):
       return max(solution.harvests, key=lambda harvest: harvest.volume).volume 