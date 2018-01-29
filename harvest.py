import random
import math

class Harvest:
    def __init__(self, number):
        self.number = number
        self.plots = []
        self.volume = 0
        self.growth_modifier = math.pow((1 + 0.3), self.number)
    
    def from_harvest(self, harvest):
        self.number = harvest.number
        self.plots = list(harvest.plots)
        self.volume = harvest.volume
    
    def add_plot(self, plot):
        self.plots.append(plot)
        self.volume += plot.volume * self.growth_modifier
    
    def remove_plot(self, plot):
        self.plots.remove(plot)
        self.volume -= plot.volume * self.growth_modifier
    
    def remove_random_plot(self):
        random_plot = random.choice(self.plots)
        self.remove_plot(random_plot)
        return random_plot
             
    def __str__(self):
        return str(self.plots)
    
    def __repr__(self):
        return str(self)