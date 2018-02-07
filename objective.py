import sys
import math
import random

from collections import deque
from solution import Solution

class Objective:
    def __init__(self, cost):
        self.cost = cost
    
    def generate_neighbor_from_base(self):
        neighbor_solution = Solution(self.base_solution.num_harvests)
        neighbor_solution.from_solution(self.base_solution)
        
        first_harvest = random.choice(neighbor_solution.harvests)
        while(len(first_harvest.plots) == 0):
            first_harvest = random.choice(neighbor_solution.harvests)
    
        swap_plot = first_harvest.remove_random_plot()
    
        second_harvest = random.choice(neighbor_solution.harvests)
        while(second_harvest == first_harvest):
            second_harvest = random.choice(neighbor_solution.harvests)
        
        second_harvest.add_plot(swap_plot)
        return neighbor_solution
    
    def compute_normalized_cost_delta(self, first_solution, second_solution):
        if (first_solution.cost is sys.maxsize):
            first_solution.cost = self.cost.calculate(first_solution)
        
        if (second_solution.cost is sys.maxsize):
            second_solution.cost = self.cost.calculate(second_solution)
            
        return (second_solution.cost / first_solution.cost) - 1
    
    
class HillClimb(Objective):
    def __init__(
        self, cost
    ):
        super(HillClimb, self).__init__(cost)
    
    def configure(self, max_iterations=100000):
        self.max_iterations = max_iterations
    
    def set_base_solution(self, solution):
        self.base_solution = solution
        self.best_solution = solution
    
    def continue_solving(self, iterations):
        return iterations < self.max_iterations
       
    def accept_solution(self, neighbor_solution):
        normalized_cost_delta = self.compute_normalized_cost_delta(self.base_solution, neighbor_solution)
        
        return normalized_cost_delta < 0
 
class SimulatedAnnealing(Objective):
    def __init__(self, cost):
        super(SimulatedAnnealing, self).__init__(cost)
        
    def configure(self, temperature=1.0, min_temperature=0.0001, alpha=0.99, repetitions=1000):
        self.temperature = temperature
        self.repetitions = repetitions
        self.alpha = alpha
        self.min_temperature = min_temperature    
        
    def set_base_solution(self, solution):
        self.base_solution = solution
        self.best_solution = solution     
        
    def continue_solving(self, iterations):
        if iterations % self.repetitions == 0:
            self.temperature = self.temperature * self.alpha
        
        return self.temperature > self.min_temperature
    
    def accept_solution(self, neighbor_solution):
        normalized_cost_delta = self.compute_normalized_cost_delta(self.base_solution, neighbor_solution)
       
        try:
            accept_probability =  1 / math.exp((normalized_cost_delta / self.temperature))
        except OverflowError:
            accept_probability = 0
            
        return random.random() < accept_probability

class ThresholdAccepting(Objective):
    def __init__(self, cost):
        super(ThresholdAccepting, self).__init__(cost)
        
    def configure(self, threshold=0.02, min_threshold=-0.02, threshold_step=0.0001, repetitions=500):
        self.threshold = threshold
        self.min_threshold = min_threshold
        self.threshold_step = threshold_step
        self.repetitions = repetitions
    
    def set_base_solution(self, solution):
        if solution.cost is sys.maxsize:
            solution.cost = self.cost.calculate(solution)
            
        self.base_solution = solution
        self.best_solution = solution
    
    def continue_solving(self, iterations):   
        if iterations % self.repetitions == 0:
            self.threshold -= self.threshold_step

        return self.threshold > self.min_threshold
        
    def accept_solution(self, neighbor_solution):
        normalized_cost_delta = self.compute_normalized_cost_delta(self.base_solution, neighbor_solution)
      
        return normalized_cost_delta < self.threshold
        
class RecordToRecord(Objective):
    def __init__(
        self, cost  
    ):
        super(RecordToRecord, self).__init__(cost)

        self.best_solution = None
    
    def configure(self, deviation=0.1, max_iterations=1000000):           
        self.deviation = deviation
        self.max_iterations = max_iterations        
    
    def set_base_solution(self, solution):
        if solution.cost is sys.maxsize:
            solution.cost = self.cost.calculate(solution)

        if self.best_solution is None:
            self.best_solution = solution
            
        self.base_solution = solution       
        
        if solution.cost < self.best_solution.cost:
            self.best_solution = solution

    
    def continue_solving(self, iterations):
        return iterations < self.max_iterations
        
    def accept_solution(self, neighbor_solution):
        if (neighbor_solution.cost is sys.maxsize):
            neighbor_solution.cost = self.cost.calculate(neighbor_solution)
            
        return neighbor_solution.cost < self.best_solution.cost * (1 + self.deviation)
    
  
class GreatEvaporation(Objective):
    def __init__(self, cost):
        super(GreatEvaporation, self).__init__(cost)

    def configure(self, evaporate=1, water_level=1000000, max_iterations=1000000):
        self.evaporate = evaporate 
        self.water_level = water_level
        
        self.max_iterations = max_iterations
    
    def set_base_solution(self, solution):
        if solution.cost is sys.maxsize:
            solution.cost = self.cost.calculate(solution)
    
        self.base_solution = solution
        self.best_solution = solution
        
    def continue_solving(self, iterations):
        return iterations < self.max_iterations
        
    def accept_solution(self, neighbor_solution):
        if (neighbor_solution.cost is sys.maxsize):
            neighbor_solution.cost = self.cost.calculate(neighbor_solution)
        
        if neighbor_solution.cost < self.water_level:
            self.water_level = self.water_level - self.evaporate
            return True
        
        return False
            

class TabuSearch(Objective):
    def __init__(
        self, cost,
        
    ):
        super(TabuSearch, self).__init__(cost)
        self.best_solution = None
        self.tabu_list = deque()
    
    def configure(self, short_term_size=10, max_iterations=1000):
        self.short_term_size = short_term_size
        self.max_iterations = max_iterations
    
    def generate_neighbor_from_base(self):
        best_cost = sys.maxsize
        best_neighbor = None
        
        for first_harvest_index in range(len(self.base_solution.harvests)):
            for second_harvest_index in range(len(self.base_solution.harvests)):
                if second_harvest_index == first_harvest_index:
                    continue
                    
                for first_harvest_plot in self.base_solution.harvests[first_harvest_index].plots:
                    neighbor_solution = Solution(self.base_solution.num_harvests)
                    neighbor_solution.from_solution(self.base_solution)
                    
                    neighbor_solution.harvests[first_harvest_index].remove_plot(first_harvest_plot)
                    neighbor_solution.harvests[second_harvest_index].add_plot(first_harvest_plot)
                    
                    if (neighbor_solution not in self.tabu_list):                   
                        neighbor_solution.cost = self.cost.calculate(neighbor_solution)
                        if (neighbor_solution.cost < best_cost):
                            best_cost = neighbor_solution.cost
                            best_neighbor = neighbor_solution
                            
        return best_neighbor
                        
    
    def set_base_solution(self, solution):
        if solution.cost is sys.maxsize:
            solution.cost = self.cost.calculate(solution)
    
        if self.best_solution is None:
            self.best_solution = solution
    
        self.base_solution = solution
        
        if (solution.cost < self.best_solution.cost):
            self.best_solution = solution
        
        self.tabu_list.appendleft(solution)
        while len(self.tabu_list) > self.short_term_size:
            self.tabu_list.pop()
        
    def continue_solving(self, iterations):
        return iterations < self.max_iterations
        
    def accept_solution(self, neighbor_solution):
        if (neighbor_solution.cost is sys.maxsize):
            neighbor_solution.cost = self.cost.calculate(neighbor_solution)
            
        return True
        
        