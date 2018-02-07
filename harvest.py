import random
import math

class Harvest:
    def __init__(self, number):
        self.number = number
        self.plots = set()
        self.volume = 0
        self.growth_modifier = math.pow((1 + 0.3), self.number)
    
    def from_harvest(self, harvest):
        self.number = harvest.number
        self.plots = set(harvest.plots)
        self.volume = harvest.volume
    
    def add_plot(self, plot):
        self.plots.add(plot)
        self.volume += plot.volume * self.growth_modifier
    
    def remove_plot(self, plot):
        self.plots.remove(plot)
        self.volume -= plot.volume * self.growth_modifier
    
    def remove_random_plot(self):
        random_plot = self.plots.pop()
        self.volume -= random_plot.volume * self.growth_modifier
        return random_plot
             
    def __str__(self):
        return str(self.plots)
    
    def __repr__(self):
        return str(self)
        
    def __eq__(self, other):
        return self.plots == other.plots
    
    def __ne__(self, other):
        return not self.__eq__(other)
        