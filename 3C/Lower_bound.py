import networkx as nx

def create_LBgraph(tasks,users):
    LB_graph=nx.DiGraph()
    total_task_content=0

    LB_graph.add_node('IOTplatform', demand=0)
    min_processing_density=min([task.processing_density for task in tasks])

    for task in tasks:
        total_task_content+=task.output_block_num*task.content.block_size

    LB_graph.add_node('source', demand=-total_task_content)
    LB_graph.add_node('destination', demand=total_task_content)

    for task in tasks:
        task_node='task'+str(task.task_id)
        #LB_graph.add_node(task_node, demand=-1*task.output_block_num*task.content.block_size)
        LB_graph.add_node(task_node, demand=0)
        LB_graph.add_edge('source', task_node, capacity=task.output_block_num*task.content.block_size, weight=0, caching_user_cost=0,
                      computing_user_cost=0, relaying_user_cost=0)

        # 把caching nodes加入图中，并添加相应的source和caching node的边
        for caching_user_id in task.caching_users:
            caching_node = 'caching' + str(caching_user_id)
            if LB_graph.has_node(caching_node):
                continue
            LB_graph.add_node(caching_node,demand=0)
            LB_graph.add_edge(task_node,caching_node,capacity=task.output_block_num*task.content.block_size,weight=0,caching_user_cost=0,computing_user_cost=0,relaying_user_cost=0)

        LB_graph.add_edge(task_node, 'IOTplatform', capacity=task.output_block_num*task.content.block_size, weight=0,caching_user_cost=0,computing_user_cost=0,relaying_user_cost=0)

        #把computing nodes加入图中，并添加相应的caching nodes和computing nodes的边
        for computing_user_id in task.avalible_users:
            computing_node = 'computing' + str(computing_user_id)
            if LB_graph.has_node(computing_node):
                continue
            LB_graph.add_node(computing_node, demand=0)
            computing_cost = users[computing_user_id].ComputingCost(1, task)

            downloading_capacity=int(users[computing_user_id].download_cellular_data_rate)
            downloading_cost = users[computing_user_id].DownloadingCost(1)  # 1 bit 的能量
            bit_cost = downloading_cost + computing_cost
            LB_graph.add_edge('IOTplatform', computing_node, capacity=downloading_capacity, weight=bit_cost,
                              caching_user_cost=0, computing_user_cost=bit_cost, relaying_user_cost=0)

            for caching_user_id in task.caching_users:
                if caching_user_id in users[computing_user_id].avalibleCooperators:
                    caching_node='caching'+str(caching_user_id)
                    if LB_graph.has_edge(caching_node, computing_node):
                        continue

                    input_capacity=int(users[computing_user_id].transmission_datarate(users[caching_user_id]))
                    inputcost = users[computing_user_id].InputCost(users[caching_user_id], 1)
                    bit_cost = inputcost[0] + computing_cost
                    caching_user_cost = inputcost[2]
                    computing_user_cost = inputcost[1] + computing_cost
                    LB_graph.add_edge(caching_node, computing_node, capacity=input_capacity, weight=bit_cost,
                                      caching_user_cost=caching_user_cost, computing_user_cost=computing_user_cost,
                                      relaying_user_cost=0)

            #增加辅助的computing node n'
            virtual_computing_node = 'computing' + str(computing_user_id)+"'"
            LB_graph.add_node(virtual_computing_node, demand=0)
            computing_capacity=int(users[computing_user_id].idle_computation_capacity/min_processing_density) #bits/sec
            LB_graph.add_edge(computing_node, virtual_computing_node, capacity=computing_capacity, weight=0,
                              caching_user_cost=0, computing_user_cost=0, relaying_user_cost=0)

        # 把relaying nodes加入图中，并添加相应的computing nodes和relaying nodes的边，以及relaying nodes和destination的边
        for relaying_user_id in task.avalible_users:
            relaying_node = 'relaying' + str(relaying_user_id)
            if LB_graph.has_node(relaying_node):
                continue
            LB_graph.add_node(relaying_node, demand=0)
            uploading_capacity=int(users[relaying_user_id].upload_cellular_data_rate)
            LB_graph.add_edge(relaying_node,'destination', capacity=uploading_capacity, weight=0,caching_user_cost=0,computing_user_cost=0,relaying_user_cost=0)

            for computing_user_id in task.avalible_users:
                if computing_user_id in users[relaying_user_id].avalibleCooperators:
                    computing_node='computing'+str(computing_user_id)+"'"
                    if LB_graph.has_edge(computing_node,relaying_node):
                        continue

                    output_capacity=int(users[computing_user_id].transmission_datarate(users[relaying_user_id]))
                    output_cost=users[computing_user_id].OutputCost(users[relaying_user_id],1)
                    bit_cost=output_cost[0]
                    relaying_user_cost=output_cost[2]
                    computing_user_cost=output_cost[1]
                    LB_graph.add_edge(computing_node,relaying_node,capacity=output_capacity, weight=bit_cost,caching_user_cost=0,computing_user_cost=computing_user_cost,relaying_user_cost=relaying_user_cost)

    return LB_graph