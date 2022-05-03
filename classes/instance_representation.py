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
        # n = amount of jobs
        self.n = len(jobs)
        # map containing change overs for (machine z, product x, product y) 
        self.change_overs = change_overs


class Machine:
    def __init__(self, index):
        self.index = index
        # {job: i, operation: j, start_time: x, end_time: y, product: "enzyme_"}
        self.operations = []

class Job:
    def __init__(self, operations, product, due):
        self.operations = operations
        self.product = product
        self.due = due
        self.is_scheduled = False
        self.s = sum(map(lambda x : x.s, operations))

class Operation:
    def __init__(self, machines):
        self.machines = machines
        self.n_machines = len(machines)
        self.s = sum(map(lambda x : x.time, machines)) / self.n_machines
        
class Op_Machine:
    def __init__(self, index, time):
        self.index = index
        self.time = time
