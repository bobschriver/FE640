import sys
import math
import random

class Objective:
    def __init__(self, cost):
        self.cost = cost
    
    def compute_normalized_cost_delta(self, first_solution, second_solution):
        if (first_solution.cost is sys.maxsize):
            first_solution.cost = self.cost.calculate(first_solution)
        
        if (second_solution.cost is sys.maxsize):
            second_solution.cost = self.cost.calculate(second_solution)
            
        return (second_solution.cost / first_solution.cost) - 1
    
    
class HillClimb(Objective):
    def __init__(
        self, cost, 
        max_iterations=100000
    ):
        super(HillClimb, self).__init__(cost)
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
    def __init__(
        self, cost,
        temperature=1.0, min_temperature=0.0001, alpha=0.99, repetitions=1000
    ):
        super(SimulatedAnnealing, self).__init__(cost)
        
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
    def __init__(
        self, cost,
        threshold=0.02, min_threshold=-0.02, threshold_step=0.0001, repetitions=500
    ):
        super(ThresholdAccepting, self).__init__(cost)
        
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
        self, cost,
        deviation=3.0, max_iterations=10000
    ):
        super(RecordToRecord, self).__init__(cost)
        
        self.deviation = deviation
        self.max_iterations = max_iterations
        
        self.best_solution = None
    
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
    def __init__(
        self, cost,
        evaporate=1, water_level=1000000, max_iterations=1000000
    ):
        super(GreatEvaporation, self).__init__(cost)
        
        self.evaporate = evaporate 
        self.water_level = water_level
        
        self.max_iterations = max_iterations
        
    def set_base_solution(self, solution):
        if solution.cost is sys.maxsize:
            solution.cost = self.cost.calculate(solution)
    
        self.base_solution = solution
        self.best_solution = solution
        
    def continue_solving(self, iterations):
        if (iterations % 1000 == 0):
            print("Water Level {}".format(self.water_level))
    
        return iterations < self.max_iterations
        
    def accept_solution(self, neighbor_solution):
        if (neighbor_solution.cost is sys.maxsize):
            neighbor_solution.cost = self.cost.calculate(neighbor_solution)
        
        if neighbor_solution.cost < self.water_level:
            self.water_level = self.water_level - self.evaporate
            return True
        
        return False
            
        