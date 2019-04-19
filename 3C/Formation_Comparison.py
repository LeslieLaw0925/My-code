import random as rand

def Random_cooperation(users,tasks):  #算法不合理，需要重新设计
    joined_users=[]
    task_ids=[i for i in range(0,len(tasks))]
    rand.shuffle(task_ids)
    total_cost=0

    for task_id in task_ids:

        task=tasks[task_id]
        content_size=task.output_block_num*task.content.block_size

        caching_user_id=rand.choice(task.caching_users)
        while caching_user_id in joined_users:
            caching_user_id=rand.choice(task.caching_users)
        joined_users.append(caching_user_id)

        computing_user_id = rand.choice(task.avalible_users)
        while computing_user_id in joined_users or computing_user_id not in users[caching_user_id].avalibleCooperators:
            print('there is a loop')
            computing_user_id = rand.choice(task.avalible_users)

        input_cost=users[computing_user_id].InputCost(users[caching_user_id],content_size)
        computing_cost=users[computing_user_id].ComputingCost(content_size,task)
        joined_users.append(computing_user_id)

        relaying_user_id = rand.choice(task.avalible_users)
        while relaying_user_id in joined_users or relaying_user_id not in users[computing_user_id].avalibleCooperators:
            print('there is a loop')
            relaying_user_id = rand.choice(task.avalible_users)


        output_cost=users[computing_user_id].OutputCost(users[relaying_user_id],content_size)
        joined_users.append(relaying_user_id)

        total_cost+=(input_cost[0]+computing_cost+output_cost[0])

    return total_cost
