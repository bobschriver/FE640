import csv
import time
import argparse

from plot import Plot
from harvest import Harvest
from solution import Solution
from cost import SSE,MinMax
from objective import HillClimb,SimulatedAnnealing,ThresholdAccepting

def solve(filename, num_harvests, objective):
    plots = []

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for plot_number, plot_volume in csv_reader:
            plots.append(Plot(int(plot_number), int(plot_volume)))


    current_solution = Solution(num_harvests=num_harvests)
    current_solution.from_plots(plots)

    iterations = 0
    while objective.continue_solving(iterations):
        neighbor_solution = current_solution.generate_neighbor()
    
        #if iterations % 1000 == 0:
        #    print(time.time())
        #    print(objective.compute_normalized_cost_delta(current_solution, neighbor_solution))
        #    print(current_solution.cost)
        #    print(neighbor_solution.cost)
        #    print()
        #    for harvest in current_solution.harvests:
        #        print(harvest.volume)
        #    print()
        #    print()
    
        #print(current_solution)
        #for harvest in current_solution.harvests:
        #        print(harvest.volume)
        #print(neighbor_solution)
        #print()
    
        if objective.accept_solution(current_solution, neighbor_solution):
            current_solution = neighbor_solution
       
        iterations += 1    

    return current_solution
    
parser = argparse.ArgumentParser()
parser.add_argument('--filename', help='CSV file containing plot numbers and current volume')
parser.add_argument('--num_harvests', type=int, help='Number of harvests to schedule')
parser.add_argument('--cost', default='minmax', choices=['minmax', 'sse'], help='Type of cost to use.' )
parser.add_argument('--objective', default='simulated_annealing', choices=['hillclimb', 'simulated_annealing', 'threshold_accepting'], help='Type of objective to use')
parser.add_argument('--sse_target', type=int, default=10000, help='Target for use with SSE cost')
args = parser.parse_args()

print(args)

cost = MinMax()

if args.cost == 'sse':
    cost = SSE(target=args.sse_target)

objective = SimulatedAnnealing(cost=cost)

if args.objective == 'hillclimb':
    objective = HillClimb(cost)
elif args.objective == 'threshold_accepting':
    objective = ThresholdAccepting(cost)
    

solution = solve(args.filename, args.num_harvests, objective)    
    
print(solution)
for i, harvest in enumerate(solution.harvests):
    print("Harvest {}: {}".format(i, harvest))
    
for i, harvest in enumerate(solution.harvests):
    print("Harvest {} volume: {}".format(i, harvest.volume))