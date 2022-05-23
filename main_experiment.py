import os
import matplotlib.pyplot as plt
from main_heuristics import heuristics_solve
from main_milp import milp_solve

a = [[(0, 23), (1, 36), (2, 47), (3, 60), (4, 70), (5, 82), (6, 92), (7, 105), (8, 115), (9, 128), (10, 138), (11, 151), (12, 161)], "Heuristic algorithm"]
b = [[(0, 22.0), (1, 33.0), (2, 43.0), (3, 55.0), (4, 68.0), (5, 82.0), (6, 96.0), (7, 114.0), (8, 128.0), (9, 144.0), (10, 160.0), (11, 180.0), (12, 193.0)], "MILP Solver, 2700 second runtime limit"]

def make_plot(solutions):
    for solution in solutions:
        x_val = list(map(lambda x : x[0], solution[0]))
        y_val = list(map(lambda x : x[1], solution[0]))
        plt.plot(x_val, y_val, marker='o', label= solution[1])
    path = os.path.join("solutions/experiments")
    plt.ylabel("Lowest makespan found")
    plt.xticks(range(0, 13))
    plt.xlabel("Instances")
    plt.legend()
    plt.savefig(path + "\\"  + "plot.png")



# Runs an experiment. 
# Name is the name of the folder where the results will be saved to.
# funcs_times_labels is a list of tuples (function, t, l) where function will be ran with time limit t and displayed with label l in the plot.
# functions should take two parameters: nr_instances and time
# nr_instances is the number of instances on which to run all functions
def run_experiment(name, funcs_times_labels, nr_instances=13):
    path = os.path.join("solutions/experiments")
    file = open(path + "/" + name + ".txt", "a")
    solutions = list(map(lambda x : (x[0](nr_instances, x[1]), x[2]), funcs_times_labels))
    for solution in solutions:
        x_val = list(map(lambda x : x[0], solution[0]))
        y_val = list(map(lambda x : x[1], solution[0]))
        file.write(solution[1] + "\n")
        file.write(str(solution[0]) + "\n")
        plt.plot(x_val, y_val, marker='o', label= solution[1])
    file.close()
    plt.ylabel("Lowest makespan found")
    plt.xticks(range(0, nr_instances))
    plt.xlabel("Instances")
    plt.legend()
    plt.savefig(path + "\\" + name + ".png")
    

make_plot([a, b])
#run_experiment("heuristics", [(heuristics_solve, 30, "Heuristic solver")])