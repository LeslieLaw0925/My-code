import networkx as nx

def createMCgraph(task,caching_members,avalible_members,users):
    MC_graph=nx.DiGraph()

    MC_graph.add_node('source',demand=-1*task.output_block_num)

    # 把caching nodes加入图中，并添加相应的source和caching node的边
    for caching_user_id in caching_members:
        caching_node='caching'+str(caching_user_id)
        MC_graph.add_node(caching_node,demand=0)
        MC_graph.add_edge('source',caching_node,capacity=task.output_block_num,weight=0,caching_user_cost=0,computing_user_cost=0,relaying_user_cost=0)

    MC_graph.add_node('IOTplatform', demand=0)
    MC_graph.add_edge('source', 'IOTplatform', capacity=task.output_block_num, weight=0,caching_user_cost=0,computing_user_cost=0,relaying_user_cost=0)


    #把computing nodes加入图中，并添加相应的caching nodes和computing nodes的边
    for computing_user_id in avalible_members:
        computing_node = 'computing' + str(computing_user_id)
        MC_graph.add_node(computing_node, demand=0)
        computing_cost = users[computing_user_id].ComputingCost(task.content.block_size, task)

        downloading_capacity=int(users[computing_user_id].download_cellular_data_rate/task.content.block_size)
        downloading_cost = users[computing_user_id].DownloadingCost(task.content.block_size)  # 1 block 的能量
        block_cost = downloading_cost + computing_cost
        MC_graph.add_edge('IOTplatform', computing_node, capacity=downloading_capacity, weight=block_cost,
                          caching_user_cost=0, computing_user_cost=block_cost, relaying_user_cost=0)

        '''if users[computing_user_id].idle_computation_capacity/task.processing_density >= users[computing_user_id].download_cellular_data_rate:
            downloading_cost=users[computing_user_id].DownloadingCost(1) #1 bit 的能量
            bit_cost = downloading_cost+computing_cost
            MC_graph.add_edge('IOTplatform', computing_node, capacity=task.output_size, weight=bit_cost,caching_user_cost=0,computing_user_cost=bit_cost,relaying_user_cost=0)
        '''

        for caching_user_id in caching_members:
            if caching_user_id in users[computing_user_id].avalibleCooperators:
                caching_node='caching'+str(caching_user_id)

                input_capacity=int(users[computing_user_id].transmission_datarate(users[caching_user_id])/task.content.block_size)
                inputcost = users[computing_user_id].InputCost(users[caching_user_id], task.content.block_size)
                block_cost = inputcost[0] + computing_cost
                caching_user_cost = inputcost[2]
                computing_user_cost = inputcost[1] + computing_cost
                MC_graph.add_edge(caching_node, computing_node, capacity=input_capacity, weight=block_cost,
                                  caching_user_cost=caching_user_cost, computing_user_cost=computing_user_cost,
                                  relaying_user_cost=0)

                '''if caching_user_id!=computing_user_id and users[computing_user_id].transmission_datarate(users[caching_user_id])> users[computing_user_id].idle_computation_capacity/task.processing_density:
                    break
                inputcost=users[computing_user_id].InputCost(users[caching_user_id],1)
                bit_cost = inputcost[0]+computing_cost
                caching_user_cost=inputcost[2]
                computing_user_cost=inputcost[1]+computing_cost
                MC_graph.add_edge(caching_node,computing_node,capacity=task.output_size, weight=bit_cost, caching_user_cost=caching_user_cost,computing_user_cost=computing_user_cost,relaying_user_cost=0)
                '''

        #增加辅助的computing node n'
        virtual_computing_node = 'computing' + str(computing_user_id)+"'"
        MC_graph.add_node(virtual_computing_node, demand=0)
        computing_capacity=int(users[computing_user_id].idle_computation_capacity/task.processing_density/task.content.block_size)
        MC_graph.add_edge(computing_node, virtual_computing_node, capacity=computing_capacity, weight=0,
                          caching_user_cost=0, computing_user_cost=0, relaying_user_cost=0)

    MC_graph.add_node('destination', demand=task.output_block_num)
    # 把relaying nodes加入图中，并添加相应的computing nodes和relaying nodes的边，以及relaying nodes和destination的边
    for relaying_user_id in avalible_members:
        relaying_node = 'relaying' + str(relaying_user_id)
        MC_graph.add_node(relaying_node, demand=0)
        uploading_capacity=int(users[relaying_user_id].upload_cellular_data_rate/task.content.block_size)
        MC_graph.add_edge(relaying_node,'destination', capacity=uploading_capacity, weight=0,caching_user_cost=0,computing_user_cost=0,relaying_user_cost=0)

        for computing_user_id in avalible_members:
            if computing_user_id in users[relaying_user_id].avalibleCooperators:
                computing_node='computing'+str(computing_user_id)+"'"

                output_capacity=int(users[computing_user_id].transmission_datarate(users[relaying_user_id])/task.content.block_size)

                output_cost=users[computing_user_id].OutputCost(users[relaying_user_id],task.content.block_size)
                block_cost=output_cost[0]
                relaying_user_cost=output_cost[2]
                computing_user_cost=output_cost[1]
                MC_graph.add_edge(computing_node,relaying_node,capacity=output_capacity, weight=block_cost,caching_user_cost=0,computing_user_cost=computing_user_cost,relaying_user_cost=relaying_user_cost)

    return MC_graph