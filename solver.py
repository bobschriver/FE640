import csv
import time
import argparse

from plot import Plot
from harvest import Harvest
from solution import Solution
from cost import SSE,MinMax,Variance
from objective import HillClimb,SimulatedAnnealing,ThresholdAccepting,RecordToRecord,GreatEvaporation

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
        neighbor_solution = objective.base_solution.generate_neighbor()
    
        if iterations % 1000 == 0:
            print("Current Solution Cost: {}".format(objective.base_solution.cost))
            print("Best Solution Cost: {}".format(objective.best_solution.cost))
            print("Nieghbor Solution Cost: {}".format(cost.calculate(neighbor_solution)))
            print()
            for i,harvest in enumerate(objective.base_solution.harvests):
                print("Harvest {} volume: {}".format(i, harvest.volume))
            print()
            print()
    
        if objective.accept_solution(neighbor_solution):
            objective.set_base_solution(neighbor_solution)
       
        iterations += 1    

    return objective.best_solution
    
parser = argparse.ArgumentParser()
parser.add_argument('--filename', help='CSV file containing plot numbers and current volume')
parser.add_argument('--num_harvests', type=int, help='Number of harvests to schedule')
parser.add_argument('--cost', default='minmax', choices=['minmax', 'sse', 'variance'], help='Type of cost to use.' )
parser.add_argument('--objective', default='simulated_annealing', choices=['hillclimb', 'simulated_annealing', 'threshold_accepting', 'record_to_record', 'great_deluge'], help='Type of objective to use')
parser.add_argument('--sse_target', type=int, default=10000, help='Target for use with SSE cost')
args = parser.parse_args()

if args.cost == 'sse':
    cost = SSE(target=args.sse_target)
elif args.cost == 'minmax':
    cost = MinMax()
elif args.cost == 'variance':
    cost = Variance()

if args.objective == 'hillclimb':
    objective = HillClimb(cost=cost)
elif args.objective == 'simulated_annealing':
    objective = SimulatedAnnealing(cost=cost)
elif args.objective == 'threshold_accepting':
    objective = ThresholdAccepting(cost=cost)
elif args.objective == 'record_to_record':
    objective = RecordToRecord(cost=cost)
elif args.objective == 'great_deluge':
    objective = GreatEvaporation(cost=cost)
    
    
solution = solve(args.filename, args.num_harvests, objective)    
    
for i, harvest in enumerate(solution.harvests):
    print("Harvest {}: {}".format(i, harvest))
    
for i, harvest in enumerate(solution.harvests):
    print("Harvest {} volume: {}".format(i, harvest.volume))