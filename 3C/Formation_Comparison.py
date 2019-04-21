import random as rand

def Random_formation(users,tasks):
    unjoined_users=[i for i in range(0,len(users))]
    task_ids=[i for i in range(0,len(tasks))]
    rand.shuffle(task_ids)
    total_cost=0

    for task in tasks:
        computing_user_id=rand.choice(list(set(task.avalible_users)&set(unjoined_users)))
        while computing_user_id==None:
            computing_user_id = rand.choice(set(task.avalible_users) & set(unjoined_users))
        computing_cost=users[computing_user_id].ComputingCost(task.content.input_size,task)
        unjoined_users.remove(computing_user_id)

        input_cost=0
        output_cost=0

        if computing_user_id not in task.caching_users:
            caching_user_id=rand.choice(list(set(task.caching_users)&set(unjoined_users)&set(users[computing_user_id].avalibleCooperators)))
            if caching_user_id==None:
                input_cost=users[computing_user_id].DownloadingCost(task.content.input_size)
            else:
                input_cost=users[computing_user_id].InputCost(users[caching_user_id],task.content.input_size)[0]
                unjoined_users.remove(caching_user_id)

        relaying_user_id=rand.choice(list(set(task.avalible_users)&set(users[computing_user_id].avalibleCooperators)&set(unjoined_users)))
        if relaying_user_id==None:
            output_cost=users[computing_user_id].OutputCost(users[computing_user_id],task.content.block_size*task.output_block_num)[0]

        else:
            output_cost=users[computing_user_id].OutputCost(users[relaying_user_id],task.content.block_size*task.output_block_num)[0]
            unjoined_users.remove(relaying_user_id)

        total_cost+=(input_cost+computing_cost+output_cost)

    return [total_cost,len(users)-len(unjoined_users)]

def Greedy_formation(users,tasks):
    total_cost=0
    unjoined_users = [i for i in range(0, len(users))]

    for task in tasks:
        min_computing_cost=0
        computing_user_id=-1
        #input_cost=0
        #output_cost=0

        for user_id in list(set(task.avalible_users)&set(unjoined_users)):
            computing_cost=users[user_id].ComputingCost(task.content.input_size,task)
            if computing_cost<min_computing_cost or min_computing_cost==0:
                min_computing_cost=computing_cost
                computing_user_id=user_id

        unjoined_users.remove(computing_user_id)

        caching_user_id=rand.choice(list(set(task.caching_users)&set(unjoined_users)))
        if caching_user_id==None:
            input_cost = users[computing_user_id].DownloadingCost(task.content.input_size)
        else:
            input_cost = users[computing_user_id].InputCost(users[caching_user_id], task.content.input_size)[0]
            unjoined_users.remove(caching_user_id)

        relaying_user_id = rand.choice(list(set(task.avalible_users) & set(users[computing_user_id].avalibleCooperators) & set(unjoined_users)))
        if relaying_user_id == None:
            output_cost = users[computing_user_id].OutputCost(users[computing_user_id],task.content.block_size * task.output_block_num)[0]
        else:
            output_cost = users[computing_user_id].OutputCost(users[relaying_user_id],task.content.block_size * task.output_block_num)[0]
            unjoined_users.remove(relaying_user_id)

        total_cost += (input_cost + min_computing_cost + output_cost)

    return [total_cost,len(users)-len(unjoined_users)]










