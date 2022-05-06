import pandas as pd

def heuristic(to_solve, csv_output):
    z = -1
    y = -1
    for j in range(0, to_solve.maxJ):
        j_all_scheduled = True
        for job in to_solve.jobs:
            j_all_scheduled = j_all_scheduled and not job.operations[j].end_time == -1

        while(not j_all_scheduled):
            TC_ = to_solve.M

            for i_ in range(0, to_solve.n):
                to_solve.isort = sorted(to_solve.jobs, key=(lambda x : x.s))  
                job_i = to_solve.isort[i_]
                i = job_i.index
                if j < job_i.n_ops and job_i.operations[j].end_time == -1:
                    op_j = job_i.operations[j]
                    for k_ in range(0, to_solve.m):
                        # ksort -> lowest changeover times avg?
                        machine_k = to_solve.machines[k_]
                        k = machine_k.index
                        if machine_k.index in map((lambda x : x.index), op_j.machines):
                            #TODO implement heuristics
                            TC = 1 

                            if(TC < TC_):
                                TC_ = TC
                                z = i
                                y = k

            if(TC_ < to_solve.M):
                selected_machine = to_solve.machines[y]
                selected_job = to_solve.jobs[z]

                current_max = current_max_func(selected_machine)
                start_time = current_max
                prev_product = prev_product_func(selected_machine, start_time)
                next_product = selected_job.product
                if not start_time == 0:
                    changeover = to_solve.change_overs.get((y, prev_product, next_product))
                    start_time = start_time + changeover
                start_time = max(start_time, selected_job.operations[j-1].end_time)
                time_taken = time_taken_func(selected_job.operations[j].machines, y)
                end_time = start_time + time_taken
                to_solve.jobs[z].operations[j].end_time = end_time
            
                to_solve.machines[y].operations.append({"Machine": y, "Job": z, "Product": next_product, "Operation": j, "Start": start_time, "Duration": time_taken, "Completion": end_time})

            j_all_scheduled = True
            for job in to_solve.jobs:
                if j < job.n_ops:
                    j_all_scheduled = j_all_scheduled and not job.operations[j].end_time == -1
            
            


    # Write results to csv
    results_unfolded = map((lambda x : x.operations), to_solve.machines)
    results = [x for y in results_unfolded for x in y]

    schedule = pd.DataFrame(results)
    schedule.to_csv(csv_output, index=False)

    return schedule



def current_max_func(machine):
    if len(machine.operations) == 0:
        return 0
    return max(list(map((lambda x : x.get("Completion")), machine.operations)))

def prev_product_func(machine, end_time):
    for o in machine.operations:
        if o.get("Completion") == end_time:
            return o.get("Product")

def time_taken_func(machines, index):
    for m in machines:
        if m.index == index:
            return m.time
