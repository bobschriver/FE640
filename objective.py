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
        max_iterations=10000
    ):
        super(HillclimbObjective, self).__init__(cost)
        self.max_iterations = max_iterations
    
    def continue_solving(self, iterations):
        return iterations < max_iterations
       
    def accept_solution(self, current_solution, neighbor_solution):
        normalized_cost_delta = self.compute_normalized_cost_delta(current_solution, neighbor_solution)
        
        return normalized_cost_delta < 0
 
class SimulatedAnnealing(Objective):
    def __init__(
        self, cost,
        temperature=1, min_temperature=0.0001, alpha=0.99, repetitions=1000
    ):
        super(SimulatedAnnealing, self).__init__(cost)
        
        self.temperature = temperature
        self.repetitions = repetitions
        self.alpha = alpha
        self.min_temperature = min_temperature

    def continue_solving(self, iterations):
        if iterations % self.repetitions == 0:
            self.temperature = self.temperature * self.alpha
        
        return self.temperature > self.min_temperature
    
    def accept_solution(self, current_solution, neighbor_solution):
        normalized_cost_delta = self.compute_normalized_cost_delta(current_solution, neighbor_solution)
       
        try:
            accept_probability =  1 / math.exp((normalized_cost_delta / self.temperature))
        except OverflowError:
            accept_probability = 0
            
        return random.random() < accept_probability

class ThresholdAccepting(Objective):
    def __init__(
        self, cost,
        threshold=0.01, min_threshold=-0.01, threshold_step=0.0001, repetitions=500
    ):
        super(ThresholdAccepting, self).__init__(cost)
        
        self.threshold = threshold
        self.min_threshold = min_threshold
        self.threshold_step = threshold_step
        self.repetitions = repetitions
    
    def continue_solving(self, iterations):   
        if iterations % self.repetitions == 0:
            self.threshold -= self.threshold_step

        return self.threshold > self.min_threshold
        
    def accept_solution(self, current_solution, neighbor_solution):
        normalized_cost_delta = self.compute_normalized_cost_delta(current_solution, neighbor_solution)
      
        return normalized_cost_delta < self.threshold