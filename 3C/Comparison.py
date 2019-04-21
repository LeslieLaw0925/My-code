import networkx as nx
import re
import copy
import itertools
import operator
import random as rand
import MC_graph

def Non_Cooperation_greedy(users,tasks):
    task_costs = []
    task_min_cost_userids=[]
    joined_users = []

    for task in tasks:
        min_cost=0
        min_cost_userid=-1

        for user_id in task.avalible_users:

            if user_id in joined_users:
                continue
            user=users[user_id]
            content_size=task.output_block_num*task.content.block_size

            computing_cost=user.ComputingCost(content_size,task)
            output_cost=user.OutputCost(user,content_size)
            total_cost=computing_cost+output_cost[0]

            if user_id not in task.caching_users:
                #if users[user_id].idle_computation_capacity/task.processing_density < users[user_id].download_cellular_data_rate:
                    #continue
                downloading_cost = user.DownloadingCost(content_size)
                total_cost+=downloading_cost

            if min_cost==0 or total_cost<min_cost:
                 min_cost=total_cost
                 min_cost_userid=user_id

        task_costs.append(min_cost)
        task_min_cost_userids.append(min_cost_userid)
        joined_users.append(min_cost_userid)

    total_task_cost=0
    for cost in task_costs:
        total_task_cost+=cost

    return total_task_cost

def Non_Cooperation(users,tasks):
    task_costs = []
    joined_users=[]

    for task in tasks:

        for user_id in task.avalible_users:
            if user_id not in joined_users:
                user=users[user_id]
                content_size=task.output_block_num*task.content.block_size

                computing_cost=user.ComputingCost(content_size,task)
                output_cost=user.OutputCost(user,content_size)
                total_cost=computing_cost+output_cost[0]

                if user_id not in task.caching_users:
                    downloading_cost = user.DownloadingCost(content_size)
                    total_cost+=downloading_cost

                joined_users.append(user_id)
                task_costs.append(total_cost)

                break

    total_task_cost=0
    for cost in task_costs:
        total_task_cost+=cost

    return total_task_cost

def RangeGreedy(tasks,users):
    joined_users=[]
    total_cost=0

    for task in tasks:
        for user_id in task.avalible_users:
            if user_id in joined_users:
                continue

            user = users[user_id]
            content_size = task.output_block_num*task.content.block_size
            computing_cost = user.ComputingCost(content_size, task)
            output_cost = user.OutputCost(user, content_size)

            if user_id not in task.caching_users:
                if user.computation_capacity/task.processing_density >= users[user_id].download_cellular_data_rate:
                    downloading_cost=user.DownloadingCost(content_size)
                    total_cost += (computing_cost + output_cost[0]+downloading_cost)
                    joined_users.append(user_id)
                    break

                else:
                    continue
            else:
                total_cost+=(computing_cost+output_cost[0])
                joined_users.append(user_id)
                break

    return total_cost

overlap_BruteSolution_cost = 0
non_overlap_BruteSolution_cost = 0
COUNT=0
overlap_brute_greedy_usernum=0
non_overlap_brute_greedy_usernum=0

def BruteGreedy(users, tasks):
    global COUNT
    global overlap_BruteSolution_cost
    global overlap_brute_greedy_usernum
    global non_overlap_BruteSolution_cost
    global non_overlap_brute_greedy_usernum

    task_ids=[i for i in range(0,len(tasks))]

    for i in range(0,50):
        rand.shuffle(task_ids)
        print('task id list is,', task_ids)
        print('the overlap_BruteSolution_cost is,', overlap_BruteSolution_cost)
        print('the non_overlap_BruteSolution_cost is,', non_overlap_BruteSolution_cost)
        overlap_total_cost=0
        non_overlap_total_cost=0

        for user in users:
            user.current_task_id = -1
            for helper_id in user.avalibleCooperators:
                user.D2D_rate_of_Cooperators[helper_id] = user.transmission_datarate(users[helper_id])

        for task_id in task_ids:
            overlap_total_cost += BruteGreedy_SingelTask(task_id, users, tasks,'overlap')

        if overlap_BruteSolution_cost == 0 or overlap_BruteSolution_cost > overlap_total_cost:
            overlap_BruteSolution_cost = overlap_total_cost
            overlap_brute_greedy_usernum = 0
            for user in users:
                if user.current_task_id != -1:
                    overlap_brute_greedy_usernum += 1

        #print('the overlap_total_cost is,', overlap_total_cost)

        for user in users:
            user.current_task_id = -1

        for task_id in task_ids:
            task_cost=BruteGreedy_SingelTask(task_id, users, tasks,'non_overlap')
            non_overlap_total_cost += task_cost

        if non_overlap_BruteSolution_cost == 0 or non_overlap_BruteSolution_cost > non_overlap_total_cost:
            non_overlap_BruteSolution_cost = non_overlap_total_cost
            non_overlap_brute_greedy_usernum = 0
            for user in users:
                if user.current_task_id != -1:
                    non_overlap_brute_greedy_usernum += 1

        #print('the non_overlap_total_cost is,', non_overlap_total_cost)

        for user in users:
            user.residual_CPU = user.idle_computation_capacity
            user.residual_download_cellular_data_rate = user.download_cellular_data_rate
            user.residual_upload_cellular_data_rate = user.upload_cellular_data_rate

def BruteGreedy_SingelTask(task_id,users,tasks,ifoverlap):
    task=tasks[task_id]

    if ifoverlap=='overlap':
        mc_graph=BruteGreedy_createMCgraph(task,task.caching_users,task.avalible_users,users)
        task_flowdict = nx.network_simplex(mc_graph, demand='demand', capacity='capacity', weight='weight')
        overlap_single_task_cost=task_flowdict[0]
        BruteGreedy_update(task, task_flowdict, users)
        return overlap_single_task_cost
    else:
        mc_graph = BruteGreedy_non_overlap_createMCgraph(task, task.caching_users, task.avalible_users, users)
        task_flowdict = nx.network_simplex(mc_graph, demand='demand', capacity='capacity', weight='weight')
        nonoverlap_single_task_cost = task_flowdict[0]
        BruteGreedy_non_overlap_update(task,task_flowdict, users)
        return nonoverlap_single_task_cost

def BruteGreedy_non_overlap_createMCgraph(task,caching_members,avalible_members,users):
    MC_graph = nx.DiGraph()

    MC_graph.add_node('source', demand=-1 * task.output_block_num)

    # 把caching nodes加入图中，并添加相应的source和caching node的边
    for caching_user_id in caching_members:
        if users[caching_user_id].current_task_id!=-1:
            continue
        caching_node = 'caching' + str(caching_user_id)
        MC_graph.add_node(caching_node, demand=0)
        MC_graph.add_edge('source', caching_node, capacity=task.output_block_num, weight=0, caching_user_cost=0,
                          computing_user_cost=0, relaying_user_cost=0)

    MC_graph.add_node('IOTplatform', demand=0)
    MC_graph.add_edge('source', 'IOTplatform', capacity=task.output_block_num, weight=0, caching_user_cost=0,
                      computing_user_cost=0, relaying_user_cost=0)

    # 把computing nodes加入图中，并添加相应的caching nodes和computing nodes的边
    for computing_user_id in avalible_members:
        if users[computing_user_id].current_task_id!=-1:
            continue
        computing_node = 'computing' + str(computing_user_id)
        MC_graph.add_node(computing_node, demand=0)
        computing_cost = users[computing_user_id].ComputingCost(task.content.block_size, task)

        downloading_capacity = int(
            users[computing_user_id].download_cellular_data_rate / task.content.block_size)
        downloading_cost = users[computing_user_id].DownloadingCost(task.content.block_size)  # 1 block 的能量
        block_cost = downloading_cost + computing_cost
        MC_graph.add_edge('IOTplatform', computing_node, capacity=downloading_capacity, weight=block_cost,
                          caching_user_cost=0, computing_user_cost=block_cost, relaying_user_cost=0)

        for caching_user_id in caching_members:
            if users[caching_user_id].current_task_id != -1:
                continue
            if caching_user_id in users[computing_user_id].avalibleCooperators:
                caching_node = 'caching' + str(caching_user_id)

                input_capacity = int(users[computing_user_id].transmission_datarate(users[caching_user_id])/ task.content.block_size)
                inputcost = users[computing_user_id].InputCost(users[caching_user_id], task.content.block_size)
                block_cost = inputcost[0] + computing_cost
                caching_user_cost = inputcost[2]
                computing_user_cost = inputcost[1] + computing_cost
                MC_graph.add_edge(caching_node, computing_node, capacity=input_capacity, weight=block_cost,
                                  caching_user_cost=caching_user_cost, computing_user_cost=computing_user_cost,
                                  relaying_user_cost=0)

        # 增加辅助的computing node n'
        virtual_computing_node = 'computing' + str(computing_user_id) + "'"
        MC_graph.add_node(virtual_computing_node, demand=0)
        computing_capacity = int(
            users[computing_user_id].idle_computation_capacity / task.processing_density / task.content.block_size)
        MC_graph.add_edge(computing_node, virtual_computing_node, capacity=computing_capacity, weight=0,
                          caching_user_cost=0, computing_user_cost=0, relaying_user_cost=0)

    MC_graph.add_node('destination', demand=task.output_block_num)
    # 把relaying nodes加入图中，并添加相应的computing nodes和relaying nodes的边，以及relaying nodes和destination的边
    for relaying_user_id in avalible_members:
        if users[relaying_user_id].current_task_id != -1:
            continue
        relaying_node = 'relaying' + str(relaying_user_id)
        MC_graph.add_node(relaying_node, demand=0)
        uploading_capacity = int(users[relaying_user_id].upload_cellular_data_rate / task.content.block_size)
        MC_graph.add_edge(relaying_node, 'destination', capacity=uploading_capacity, weight=0, caching_user_cost=0,
                          computing_user_cost=0, relaying_user_cost=0)

        for computing_user_id in avalible_members:
            if users[computing_user_id].current_task_id != -1:
                continue
            if computing_user_id in users[relaying_user_id].avalibleCooperators:
                computing_node = 'computing' + str(computing_user_id) + "'"

                output_capacity = int(users[computing_user_id].transmission_datarate(users[relaying_user_id])/ task.content.block_size)

                output_cost = users[computing_user_id].OutputCost(users[relaying_user_id], task.content.block_size)
                block_cost = output_cost[0]
                relaying_user_cost = output_cost[2]
                computing_user_cost = output_cost[1]
                MC_graph.add_edge(computing_node, relaying_node, capacity=output_capacity, weight=block_cost,
                                  caching_user_cost=0, computing_user_cost=computing_user_cost,
                                  relaying_user_cost=relaying_user_cost)

    return MC_graph

def BruteGreedy_non_overlap_update(task,current_flowdict,users):
    min_cost, flowdict = current_flowdict
    modified_caching_members = []
    modified_avalible_members = []

    residual_flowdict = sorted([(u, v) for u in flowdict for v in flowdict[u] if flowdict[u][v] > 0])

    # 筛选出有流量通过的边
    for u, v in residual_flowdict:
        u_id = re.sub('\D', '', u)
        v_id = re.sub('\D', '', v)
        u_function = ''
        v_function = ''
        u_function = u_function.join(re.findall(r'[A-Za-z]', u))
        v_function = v_function.join(re.findall(r'[A-Za-z]', v))

        if u_function == 'caching' or u_function == 'computing' or u_function == 'relaying':
            user_id = int(u_id)
            users[user_id].current_task_id = task.task_id
            if user_id not in modified_avalible_members:
                modified_avalible_members.append(user_id)
                if u_function == 'caching' and user_id not in modified_caching_members:
                    modified_caching_members.append(user_id)

        if v_function == 'caching' or v_function == 'computing' or v_function == 'relaying':
            user_id = int(v_id)
            users[user_id].current_task_id = task.task_id
            if user_id not in modified_avalible_members:
                modified_avalible_members.append(user_id)
                if v_function == 'caching' and user_id not in modified_caching_members:
                    modified_caching_members.append(user_id)


def BruteGreedy_createMCgraph(task,caching_members,avalible_members,users):
    MC_graph = nx.DiGraph()

    MC_graph.add_node('source', demand=-1 * task.output_block_num)

    # 把caching nodes加入图中，并添加相应的source和caching node的边
    for caching_user_id in caching_members:
        caching_node = 'caching' + str(caching_user_id)
        MC_graph.add_node(caching_node, demand=0)
        MC_graph.add_edge('source', caching_node, capacity=task.output_block_num, weight=0, caching_user_cost=0,
                          computing_user_cost=0, relaying_user_cost=0)

    MC_graph.add_node('IOTplatform', demand=0)
    MC_graph.add_edge('source', 'IOTplatform', capacity=task.output_block_num, weight=0, caching_user_cost=0,
                      computing_user_cost=0, relaying_user_cost=0)

    # 把computing nodes加入图中，并添加相应的caching nodes和computing nodes的边
    for computing_user_id in avalible_members:
        computing_node = 'computing' + str(computing_user_id)
        MC_graph.add_node(computing_node, demand=0)
        computing_cost = users[computing_user_id].ComputingCost(task.content.block_size, task)

        downloading_capacity = int(users[computing_user_id].residual_download_cellular_data_rate / task.content.block_size)
        downloading_cost = users[computing_user_id].DownloadingCost(task.content.block_size)  # 1 block 的能量
        block_cost = downloading_cost + computing_cost
        MC_graph.add_edge('IOTplatform', computing_node, capacity=downloading_capacity, weight=block_cost,
                          caching_user_cost=0, computing_user_cost=block_cost, relaying_user_cost=0)

        for caching_user_id in caching_members:
            if caching_user_id in users[computing_user_id].avalibleCooperators:
                caching_node = 'caching' + str(caching_user_id)

                input_capacity = int(users[computing_user_id].D2D_rate_of_Cooperators[caching_user_id] / task.content.block_size)
                inputcost = users[computing_user_id].InputCost(users[caching_user_id], task.content.block_size)
                block_cost = inputcost[0] + computing_cost
                caching_user_cost = inputcost[2]
                computing_user_cost = inputcost[1] + computing_cost
                MC_graph.add_edge(caching_node, computing_node, capacity=input_capacity, weight=block_cost,
                                  caching_user_cost=caching_user_cost, computing_user_cost=computing_user_cost,
                                  relaying_user_cost=0)

        # 增加辅助的computing node n'
        virtual_computing_node = 'computing' + str(computing_user_id) + "'"
        MC_graph.add_node(virtual_computing_node, demand=0)
        computing_capacity = int(users[computing_user_id].residual_CPU/ task.processing_density / task.content.block_size)
        MC_graph.add_edge(computing_node, virtual_computing_node, capacity=computing_capacity, weight=0,
                          caching_user_cost=0, computing_user_cost=0, relaying_user_cost=0)

    MC_graph.add_node('destination', demand=task.output_block_num)
    # 把relaying nodes加入图中，并添加相应的computing nodes和relaying nodes的边，以及relaying nodes和destination的边
    for relaying_user_id in avalible_members:
        relaying_node = 'relaying' + str(relaying_user_id)
        MC_graph.add_node(relaying_node, demand=0)
        uploading_capacity = int(users[relaying_user_id].residual_upload_cellular_data_rate / task.content.block_size)
        MC_graph.add_edge(relaying_node, 'destination', capacity=uploading_capacity, weight=0, caching_user_cost=0,
                          computing_user_cost=0, relaying_user_cost=0)

        for computing_user_id in avalible_members:
            if computing_user_id in users[relaying_user_id].avalibleCooperators:
                computing_node = 'computing' + str(computing_user_id) + "'"

                output_capacity = int(users[computing_user_id].D2D_rate_of_Cooperators[relaying_user_id] / task.content.block_size)

                output_cost = users[computing_user_id].OutputCost(users[relaying_user_id], task.content.block_size)
                block_cost = output_cost[0]
                relaying_user_cost = output_cost[2]
                computing_user_cost = output_cost[1]
                MC_graph.add_edge(computing_node, relaying_node, capacity=output_capacity, weight=block_cost,
                                  caching_user_cost=0, computing_user_cost=computing_user_cost,
                                  relaying_user_cost=relaying_user_cost)

    return MC_graph

def BruteGreedy_update(task,current_flowdict,users):
    min_cost, flowdict=current_flowdict

    residual_flowdict=sorted([(u, v) for u in flowdict for v in flowdict[u] if flowdict[u][v] > 0])

   #筛选出有流量通过的边
    for u,v in residual_flowdict:
        u_id = re.sub('\D','', u)
        v_id = re.sub('\D','', v)
        u_function = ''
        v_function = ''
        u_function = u_function.join(re.findall(r'[A-Za-z]', u))
        v_function = v_function.join(re.findall(r'[A-Za-z]', v))
        flow_size=flowdict[u][v]

        if u_function=='caching'or u_function=='computing'or u_function=='relaying':
            user_id = int(u_id)
            users[user_id].current_task_id=task.task_id

        if v_function == 'caching' or v_function == 'computing' or v_function == 'relaying':
            user_id = int(v_id)
            users[user_id].current_task_id = task.task_id

        if u_function=='IOTplatform' and v_function=='computing':
            user_id = int(v_id)
            users[user_id].residual_CPU-=int(task.processing_density*flow_size*task.content.block_size)
            if users[user_id].residual_CPU<0:
                users[user_id].residual_CPU=0

            users[user_id].residual_download_cellular_data_rate-=flow_size*task.content.block_size
            if users[user_id].residual_download_cellular_data_rate<0:
                users[user_id].residual_download_cellular_data_rate=0

        if u_function=='caching' and v_function=='computing':
            caching_user_id = int(u_id)
            computing_user_id=int(v_id)

            if caching_user_id!=computing_user_id:
                caching_user=users[caching_user_id]
                computing_user=users[computing_user_id]

                caching_user.D2D_rate_of_Cooperators[computing_user_id]-=flow_size*task.content.block_size
                if caching_user.D2D_rate_of_Cooperators[computing_user_id]<0:
                    caching_user.D2D_rate_of_Cooperators[computing_user_id]=0

                computing_user.D2D_rate_of_Cooperators[caching_user_id] -= flow_size * task.content.block_size
                if computing_user.D2D_rate_of_Cooperators[caching_user_id]<0:
                    computing_user.D2D_rate_of_Cooperators[caching_user_id]=0

            users[computing_user_id].residual_CPU -= flow_size * task.processing_density * task.content.block_size
            if users[computing_user_id].residual_CPU<0:
                users[computing_user_id].residual_CPU=0

        if u_function == 'relaying' and v_function == 'destination':
            user_id = int(u_id)
            users[user_id].residual_upload_cellular_data_rate -= flow_size * task.content.block_size
            if users[user_id].residual_upload_cellular_data_rate<0:
                users[user_id].residual_upload_cellular_data_rate=0

        if u_function=='computing' and v_function=='relaying':
            computing_user_id=int(u_id)
            relaying_user_id=int(v_id)

            if computing_user_id!=relaying_user_id:
                users[computing_user_id].D2D_rate_of_Cooperators[relaying_user_id] -= flow_size * task.content.block_size
                if users[computing_user_id].D2D_rate_of_Cooperators[relaying_user_id]<0:
                    users[computing_user_id].D2D_rate_of_Cooperators[relaying_user_id]=0

                users[relaying_user_id].D2D_rate_of_Cooperators[computing_user_id] -= flow_size * task.content.block_size
                if users[relaying_user_id].D2D_rate_of_Cooperators[computing_user_id]<0:
                    users[relaying_user_id].D2D_rate_of_Cooperators[computing_user_id]=0

def BruteForce(tasks,users):
    task_permutations=itertools.permutations([i for i in range(0,len(tasks))],len(tasks))
    min_costs=[]
    for task_permutation in task_permutations:
        required_CPU=None
        total_cost=0
        task_permutation_satisfied=True
        for i in task_permutation:
            #global required_CPU
            task=tasks[i]
            different_costs=Partition_of_computing_user(-1, users, task.output_size, 'computing', task.avalible_users, task)

            if len(different_costs)==0:
                task_permutation_satisfied=False
                break

            different_costs.sort(key=operator.itemgetter(0))
            min_cost_tuple = different_costs[0]

            min_cost = min_cost_tuple[0]
            permuation=min_cost_tuple[1]
            content_partition=min_cost_tuple[2]
            required_CPU=min_cost_tuple[3]

            total_cost+=min_cost

            for i in range(0,len(permuation)):
                users[permuation[i]].residual_CPU-=required_CPU[i]

            print('task %d\'s output size is %d' % (task.task_id, task.output_block_num*task.content.block_size))
            print('task %d\'s min cost is %f' % (task.task_id, min_cost))
            print('required computing users are' ,permuation)
            print('the content partition is', content_partition)
            print('corresponding required CPU resources are', required_CPU)

        if task_permutation_satisfied:
            min_costs.append(total_cost)

        for user in users:
            user.residual_CPU=user.idle_computation_capacity


    min_tasks_cost=min(min_costs)
    return min_tasks_cost

def Partition_of_computing_user(computing_user_id,users,partition_size,user_function,function_users,task):
    function_user_number=len(function_users)
    different_costs=[]

    for user_number in range(1,function_user_number+1):
        if user_number>partition_size:
            break

        permutations = itertools.permutations(function_users, user_number)

        for permutation in permutations:
            permutation_satisfied=True
            partition = [0 for i in range(0, user_number)]
            partitions=[]
            Content_partition(partition_size, 0, partition,user_number,partitions)
            print('permutation is',permutation)
            print('corresponding partitions are',partitions)

            required_CPU = [0 for i in range(0, user_number)]

            for content_partition in partitions:
                #遍历每一种output size划分的情况
                content_partition_satisfied=True

                if user_function=='computing':
                    #print('current_user_function is computing')
                    total_cost = 0

                    for i in range(0, user_number):
                        caching_users=copy.deepcopy(task.caching_users)
                        caching_users.append(-1)
                        relaying_users=copy.deepcopy(task.avalible_users)

                        different_input_costs=Partition_of_computing_user(permutation[i], users, content_partition[i], 'input', caching_users,task)

                        if len(different_input_costs)==0:
                            content_partition_satisfied=False
                            break

                        different_input_costs.sort(key=operator.itemgetter(0))
                        min_input_cost_tuple=different_input_costs[0]
                        min_input_cost,required_CPU[i]=min_input_cost_tuple

                        # 更新computing user的剩余CPU资源
                        #users[permutation[i]].residual_CPU-=required_CPU[i]

                        different_output_costs=Partition_of_computing_user(permutation[i], users, content_partition[i], 'output', relaying_users,task)
                        min_output_cost=min(different_output_costs)
                        total_cost+=(min_input_cost+min_output_cost)

                    if content_partition_satisfied:
                        cost_tuple=(total_cost, copy.deepcopy(permutation), copy.deepcopy(content_partition),copy.deepcopy(required_CPU))
                        different_costs.append(cost_tuple)
                        print(cost_tuple)
                        #for i in range(0, user_number):
                            #users[permutation[i]].residual_CPU += required_CPU[i]

                elif user_function=='input':
                    computing_user=users[computing_user_id]
                    max_required_CPU=0
                    total_cost = 0

                    #print('current_user_function is input')
                    for i in range(0,user_number):

                        if permutation[i]==-1 and computing_user.residual_CPU/task.processing_density >= computing_user.download_cellular_data_rate:
                            #意味着computing user从IOT platform下载数据
                            print('downloading is involved.')
                            total_cost+=computing_user.DownloadingCost(1)*content_partition[i]
                            total_cost+=computing_user.ComputingCost(1,task)*content_partition[i]

                            print('current_content_partition is', content_partition)
                            print('current min cost is', total_cost)

                            if max_required_CPU<=task.processing_density*computing_user.download_cellular_data_rate or max_required_CPU==0:
                                max_required_CPU=int(task.processing_density*computing_user.download_cellular_data_rate)

                        elif permutation[i]!=-1 and computing_user.transmission_datarate(users[permutation[i]]) <= computing_user.residual_CPU / task.processing_density:
                            print('D2D caching is involved.')
                            input_cost=computing_user.InputCost(users[permutation[i]],1)
                            total_cost+=input_cost[0]*content_partition[i]
                            total_cost += computing_user.ComputingCost(1, task)*content_partition[i]

                            if max_required_CPU<=task.processing_density * computing_user.transmission_datarate(users[permutation[i]]) or max_required_CPU==0:
                                max_required_CPU=int(task.processing_density*computing_user.transmission_datarate(users[permutation[i]]))

                        else:
                            permutation_satisfied=False
                            print('current permutation is unsatisfied')
                            break

                    if permutation_satisfied:
                        different_costs.append((total_cost,max_required_CPU))
                    else:
                        break

                elif user_function=='output':
                    computing_user = users[computing_user_id]
                    total_cost = 0
                    #print('current_user_function is output')

                    for i in range(0,user_number):
                        output_cost=computing_user.OutputCost(users[permutation[i]],1)
                        total_cost += output_cost[0]*content_partition[i]

                    different_costs.append(total_cost)

    return different_costs


def Content_partition(content_size, residual_computing_number, partition,computing_number,partitions):
    #print('content partition is functioning.')
    if content_size == 0 and residual_computing_number == computing_number:
        partition=sorted(partition)
        if partition not in partitions:
            partitions.append(partition)

    elif content_size >0 and residual_computing_number < computing_number:
        for i in range(1, content_size + 1):
            for j in range(residual_computing_number, computing_number):
                partition[j] = i
                Content_partition(content_size-i, residual_computing_number+1, copy.deepcopy(partition),computing_number,partitions)





