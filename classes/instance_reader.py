from classes.instance_representation import Job, Machine, Op_Machine, Operation, ToSolve


def read_instance(jobs, machines, processingTimes, machineAlternatives, operations, changeOvers, orders):
    result_jobs = []
    for j in jobs:
        order = orders.get(j)
        product = order.get('product')
        due = order.get('due')
        job_ops = operations.get(j)
        result_ops = []
       
        for o in job_ops:
            op_machines = machineAlternatives.get((j,o))
            result_machines = []
            for m in op_machines:
               time = processingTimes.get((j,o,m))
               result_machines.append(Op_Machine(m, time))

            result_ops.append(Operation(o, result_machines))
        
        result_jobs.append(Job(j, result_ops, product, due))
    
    result_machines = []
    for m in machines:
        result_machines.append(Machine(m))

    
    return ToSolve(result_jobs, result_machines, changeOvers)
