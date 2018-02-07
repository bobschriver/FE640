import csv
import time
import argparse
import json

from plot import Plot
from harvest import Harvest
from solution import Solution
from cost import SSE,MinMax,Variance
from objective import HillClimb,SimulatedAnnealing,ThresholdAccepting,RecordToRecord,GreatEvaporation,TabuSearch

def solve(filename, num_harvests, objective):
    plots = []

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for plot_number, plot_volume in csv_reader:
            plots.append(Plot(int(plot_number), int(plot_volume)))


    init_solution = Solution(num_harvests=num_harvests)
    init_solution.from_plots(plots)

    objective.set_base_solution(init_solution)
    
    iterations = 0
    while objective.continue_solving(iterations):
        neighbor_solution = objective.generate_neighbor_from_base()
    
        if iterations % 1000 == 0:
            print()
            print("Iterations: {}".format(iterations))
            print("Current Solution Cost: {}".format(objective.base_solution.cost))
            print("Best Solution Cost: {}".format(objective.best_solution.cost))
            print("Nieghbor Solution Cost: {}".format(cost.calculate(neighbor_solution)))
            print()
            for i,harvest in enumerate(objective.base_solution.harvests):
                print("Harvest {} volume: {}".format(i, harvest.volume))
            print()
    
        if objective.accept_solution(neighbor_solution):
            objective.set_base_solution(neighbor_solution)
       
        iterations += 1    

    return objective.best_solution

cost_choices = {
    'minmax': MinMax,
    'sse': SSE,
    'variance': Variance,
    }
    
objective_choices = {
    'hillclimb': HillClimb, 
    'simulated_annealing': SimulatedAnnealing, 
    'threshold_accepting': ThresholdAccepting, 
    'record_to_record': RecordToRecord, 
    'great_evaporation': GreatEvaporation, 
    'tabu_search': TabuSearch
    }
    
parser = argparse.ArgumentParser()
parser.add_argument('--filename', help='CSV file containing plot numbers and current volume')
parser.add_argument('--num_harvests', type=int, help='Number of harvests to schedule')
parser.add_argument('--configuration', help='JSON file containing configuration for cost function & objective function')
args = parser.parse_args()

configuration = json.load(open(args.configuration))

cost_configuration = configuration['cost']
cost = cost_choices[cost_configuration['cost_function']]()
cost.configure(**cost_configuration['parameters'])

objective_configuration = configuration['objective']
objective = objective_choices[objective_configuration['objective_function']](cost)
objective.configure(**objective_configuration['parameters'])
    
    
solution = solve(args.filename, args.num_harvests, objective)    
    
for i, harvest in enumerate(solution.harvests):
    print("Harvest {}: {}".format(i, harvest))
    
for i, harvest in enumerate(solution.harvests):
    print("Harvest {} volume: {}".format(i, harvest.volume))