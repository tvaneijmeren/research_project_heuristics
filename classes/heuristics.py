from copy import deepcopy
import time
import pandas as pd

def heuristic_slow(to_solve, csv_output):
    s_time = time.perf_counter()
    cmax = to_solve.M
    results = []
    to_solve_original = to_solve
    for w1 in [4,6,8, 10]:
        for w2 in range(-3, -2):
            for w3 in range(-4, -3):
                for w4 in range(-2, 1):
                    for w5 in range(-3, -2):
                                w6 = 1
                                w7 = 1
                                to_solve = deepcopy(to_solve_original)
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
                                            ii = (1 - w6) * i_ + w6 * (to_solve.n - 1 - i_) 
                                            job_i = to_solve.isort[ii]
                                            i = job_i.index
                                            if j < job_i.n_ops and job_i.operations[j].end_time == -1:
                                                op_j = job_i.operations[j]
                                                for k_ in range(0, to_solve.m):
                                                    # ksort -> lowest changeover times avg?
                                                    ki = (1 - w7) * k_ + w7 * (to_solve.m - 1 - k_) 
                                                    machine_k = to_solve.machines[ki]
                                                    k = machine_k.index
                                                    if machine_k.index in map((lambda x : x.index), op_j.machines):
                                                        #TODO implement heuristics
                                                        end_time_prev_op = 0
                                                        if j > 0:
                                                            end_time_prev_op = job_i.operations[j-1].end_time
                                                        current_max = current_max_func(machine_k)
                                                        time_taken =  time_taken_func(op_j.machines, k)
                                                        h1 = max(current_max, end_time_prev_op) + time_taken
                                                        h2 = max(0, end_time_prev_op - current_max)
                                                        h3 = max(0, current_max - end_time_prev_op)
                                                        h4 = time_taken
                                                        h5 = job_i.s
                                                        TC = w1 * h1 + w2 * h2 + w3 * h3 + w4 * h4 + w5 * h5
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
                            
                                temp_results_unfolded = map((lambda x : x.operations), to_solve.machines)
                                temp_results = [x for y in temp_results_unfolded for x in y]
                                temp_cmax = max(list(map((lambda x : x.get("Completion")),  temp_results)))
                                
                                if temp_cmax < cmax:
                                    cmax = temp_cmax
                                    results = temp_results
                                    w1_r = w1
                                    w2_r = w2 
                                    w3_r = w3 
                                    w4_r = w4 
                                    w5_r = w5 
                                    w6_r = w6
                                    w7_r = w7

    # Write results to csv
    schedule = pd.DataFrame(results)
    schedule.to_csv(csv_output, index=False)
    print(w1_r, w2_r, w3_r, w4_r, w5_r, w6_r, w7_r)
    c_time = time.perf_counter() - s_time
    print(f"{c_time:0.4f} seconds")
    return schedule


def heuristic_fast(to_solve, csv_output):
    s_time = time.perf_counter()
    w1 = 6
    w2 = 0
    w3 = -1
    w4 = -2
    w5 = -3

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
                            end_time_prev_op = 0
                            if j > 0:
                                end_time_prev_op = job_i.operations[j-1].end_time
                            current_max = current_max_func(machine_k)
                            time_taken =  time_taken_func(op_j.machines, k)
                            h1 = max(current_max, end_time_prev_op) + time_taken
                            h2 = max(0, end_time_prev_op - current_max)
                            h3 = max(0, current_max - end_time_prev_op)
                            h4 = time_taken
                            h5 = job_i.s
                            TC = w1 * h1 + w2 * h2 + w3 * h3 + w4 * h4 + w5 * h5
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
        
    results_unfolded = map((lambda x : x.operations), to_solve.machines)
    results = [x for y in results_unfolded for x in y]
    schedule = pd.DataFrame(results)
    schedule.to_csv(csv_output, index=False)
    c_time = time.perf_counter() - s_time
    print(f"{c_time:0.4f} seconds")
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
