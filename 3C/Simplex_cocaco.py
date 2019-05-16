from pulp import *

def Energy_min(users,tasks):
    user_num=len(users)
    task_num=len(tasks)

    prob_energy_min=LpProblem('energy_min',LpMinimize)

    binary_variables=dict()

    for task_id in range(0,len(tasks)):
        for user_id in range(0,len(users)):
            down_variable='down'+str(task_id)+','+str(user_id)
            binary_variables[down_variable]=0

            cpu_variable='cpu'+str(task_id)+','+str(user_id)
            binary_variables[cpu_variable]=0

            for user_id_m in range(0,len(users)):
                input_variable='input'+str(task_id)+','+str(user_id)+','+str(user_id_m)
                binary_variables[input_variable]=0

                output_variable='output'+str(task_id)+','+str(user_id)+','+str(user_id_m)
                binary_variables[output_variable]=0

    variables=LpVariable.dicts('binary_variables',binary_variables,0,None,LpBinary)

    energy_min=0
    for k in range(task_num):
        energy_min +=lpSum(variables['down'+str(k)+','+str(i)]*users[i].DownloadingCost(tasks[k].output_block_num*tasks[k].content.block_size) for i in tasks[k].avalible_users)

        energy_min += lpSum(variables['cpu' + str(k) + ',' + str(i)] * users[i].ComputingCost(
            tasks[k].output_block_num * tasks[k].content.block_size, tasks[k]) for i in tasks[k].avalible_users)

        energy_min +=lpSum([variables['input'+str(k)+','+str(i)+','+str(j)]*users[i].InputCost(users[j],tasks[k].output_block_num*tasks[k].content.block_size)[0] for j in users[i].avalibleCooperators] for i in tasks[k].avalible_users)

        energy_min += lpSum([variables['output'+str(k)+','+str(i)+','+str(j)]* users[i].OutputCost(users[j],tasks[k].output_block_num*tasks[k].content.block_size)[0] for j in users[i].avalibleCooperators] for i in tasks[k].avalible_users)

    prob_energy_min+=energy_min

    for i in range(user_num):
        #(2)
        prob_energy_min +=lpSum(variables['down'+str(k)+','+str(i)]*tasks[k].content.block_size*tasks[k].content.input_block_num for k in users[i].avalibleTasks) <= users[i].download_cellular_data_rate

        for k in users[i].avalibleTasks:
            if_cache=0
            if i in tasks[k].caching_users:
                if_cache=1
            #(3)
            prob_energy_min += variables['down'+str(k)+','+str(i)] <= if_cache

    for i in range(user_num):
        for j in users[i].avalibleCooperators:
            #(5)
            prob_energy_min +=lpSum(variables['input'+str(k)+','+str(i)+','+str(j)]*tasks[k].content.input_block_num*tasks[k].content.block_size for k in users[j].avalibleTasks) <= users[j].transmission_datarate(users[i])

            for k in users[i].avalibleTasks:
                if_cache = 0
                if i in tasks[k].caching_users:
                    if_cache = 1
                #(6)
                prob_energy_min += variables['input'+str(k)+','+str(i)+','+str(j)] <= if_cache

    for i in range(user_num):
        #(8)
        prob_energy_min += lpSum(variables['cpu'+str(k)+','+str(i)]*tasks[k].content.input_block_num*tasks[k].content.block_size*tasks[k].processing_density for k in users[i].avalibleTasks) <= users[i].idle_computation_capacity
        #增加约束：一个user只能服务一个task
        #prob_energy_min += lpSum(variables['cpu' + str(k) + ',' + str(i)] for k in users[i].avalibleTasks) == 1

    for k in range(task_num):
        #(9)
        prob_energy_min += lpSum(variables['cpu' + str(k) + ',' + str(i)] for i in tasks[k].avalible_users)==1

        for i in tasks[k].avalible_users:
            #(10)
            prob_energy_min += variables['down'+str(k)+','+str(i)]+ lpSum(variables['input'+str(k)+','+str(i)+','+str(j)] for j in users[i].avalibleCooperators)==variables['cpu'+str(k)+','+str(i)]

            #(15)
            prob_energy_min +=variables['cpu'+str(k)+','+str(i)]==lpSum(variables['output'+str(k)+','+str(i)+','+str(j)] for j in users[i].avalibleCooperators)


    for i in range(user_num):
        for j in users[i].avalibleCooperators:
            #(13)
            prob_energy_min += lpSum(variables['output'+str(k)+','+str(i)+','+str(j)] * tasks[k].output_block_num*tasks[k].content.block_size for k in users[i].avalibleTasks) <= users[i].transmission_datarate(users[j])

        #(14)
        prob_energy_min += lpSum([
            variables['output' + str(k) + ',' + str(j) + ',' + str(i)] * tasks[k].output_block_num * tasks[k].content.block_size for k in users[j].avalibleTasks] for j in users[i].avalibleCooperators) <= users[i].upload_cellular_data_rate

    #prob_energy_min.writeLP('energy_min.lp')
    prob_energy_min.solve()

    return value(prob_energy_min.objective)