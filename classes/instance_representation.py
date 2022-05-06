class ToSolve:
    def __init__(self, jobs, machines, change_overs):
        # max operations for a single job --> constant 3.   
        self.maxJ = 3
        # a large number --> value chosen, note in paper, can be optimized later.
        self.M = 1000
        # list of machines
        self.machines = machines
        # list of jobs
        self.jobs = jobs
        # list of jobs sorted on s value increasing. 
        #TODO why increasing? --> just do as in paper for now change later potentially
        self.isort = sorted(jobs, key=(lambda x : x.s))  
        # n = amount of jobs
        self.n = len(jobs)
        # m = amount of machines
        self.m = len(machines)
        # map containing change overs for (machine z, product x, product y) 
        self.change_overs = change_overs


class Machine:
    def __init__(self, index):
        self.index = index
        # {job: i, operation: j, start_time: x, end_time: y, product: "enzyme_"}
        self.operations = []

class Job:
    def __init__(self, index, operations, product, due):
        self.index = index 
        self.operations = operations
        self.n_ops = len(operations)
        self.product = product
        self.due = due
        self.s = sum(map(lambda x : x.s, operations))

class Operation:
    def __init__(self, index, op_machines):
        self.index = index
        self.machines = op_machines
        self.n_machines = len(op_machines)
        self.end_time = -1
        self.s = sum(map(lambda x : x.time, op_machines)) / self.n_machines
        
class Op_Machine:
    def __init__(self, index, time):
        self.index = index
        self.time = time
