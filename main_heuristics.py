import importlib
from classes.heuristics import heuristic
from classes.instance_reader import read_instance
from classes.instance_representation import ToSolve
from main_milp import objective_function


def run_heuristics(fileName, time=0):
    spec = importlib.util.spec_from_file_location('instance', "instances/" + fileName + '.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    to_solve = read_instance(jobs=mod.jobs, machines=mod.machines, processingTimes=mod.processingTimes,
                          machineAlternatives=
                          mod.machineAlternatives, operations=mod.operations,
                          changeOvers=mod.changeOvers, orders=mod.orders)
    return heuristic(to_solve, "solutions/heuristic/heuristic_solution_" + fileName + '.csv')


def heuristics_solve(nr_instances, time):
    solution = []
    for i in range(0, nr_instances):
        file_name = 'FJSP_' + str(i)
        try:
            s = run_heuristics(file_name, time)
            m = objective_function(s)
            solution.append((i, m))
        except:
            # Currently: store nothing in case no feasible solution is found in the time limit
            pass
    return solution