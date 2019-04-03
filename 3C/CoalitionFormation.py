import MC_graph
import networkx as nx
import copy
import re
from User import User

def coalitionFormation(users,tasks):

    ifcontinue=True
    iteration=0

    while ifcontinue:
        ifcoalitionchange1,iteration=joining(users,tasks,iteration)
        ifcoalitionchange2,iteration=switching(users,tasks,iteration)
        ifcoalitionchange3,iteration=retreating(users,tasks,iteration)

        if ifcoalitionchange1==False and ifcoalitionchange2==False and ifcoalitionchange3==False:
            ifcontinue=False

    total_task_cost=0
    for task in tasks:
        total_task_cost+=task.current_flowdict[0]

    total_participated_usernum=0
    for user in users:
        if user.current_task_id!=-1:
            total_participated_usernum+=1

    return [total_task_cost,total_participated_usernum,iteration]

def joining(users,tasks,iteration):
    ifcoalitionchange=False
    for user_id in range(0,len(users)):
        user=users[user_id]
        if user.current_task_id==-1:
            min_cost_taskid = -1
            min_cost = 50*User.exponent

            for task_id in user.avalibleTasks:
                task=tasks[task_id]
                task.current_avalible_users.append(user.user_id)
                if task.ifCoalitionExist(task.current_avalible_users)==True:
                    task.current_avalible_users.remove(user.user_id)
                    continue

                if user.user_id in task.caching_users:
                    task.current_caching_users.append(user.user_id)

                mc_graph=MC_graph.createMCgraph(task,task.current_caching_users,task.current_avalible_users,users)
                flowdict=nx.network_simplex(mc_graph, demand='demand', capacity='capacity', weight='weight')

                if flowdict[0]<min_cost and flowdict[0]<task.current_flowdict[0]:
                    min_cost=flowdict[0]
                    min_cost_taskid=task.task_id

                task.current_avalible_users.remove(user.user_id)
                if user.user_id in task.caching_users:
                    task.current_caching_users.remove(user.user_id)

            if min_cost!=50*User.exponent and min_cost_taskid!=-1:
                ifcoalitionchange=True
                iteration+=1
                task=tasks[min_cost_taskid]
                task.current_avalible_users.append(user.user_id)
                if user.user_id in task.caching_users:
                    task.current_caching_users.append(user.user_id)

                mc_graph = MC_graph.createMCgraph(task, task.current_caching_users, task.current_avalible_users,users)
                flowdict = nx.network_simplex(mc_graph, demand='demand', capacity='capacity', weight='weight')

                print('task %d\'s coalition is'%task.task_id)
                print(flowdict)
                print('user %d has joined task %d' % (
                    user.user_id, task.task_id))
                removeUnused(task,flowdict,users)
                print('after removing, task %d\'s coalition is'% task.task_id)
                print(task.current_avalible_users)
                print('after removing, task %d\'s caching users are' % task.task_id)
                print(task.current_caching_users)

    return (ifcoalitionchange,iteration)

def switching(users,tasks,iteration):
    ifcoalitionchange=False

    for user_id in range(0,len(users)):
        for switcher_id in users[user_id].avalibleCooperators:
            user=users[user_id]
            if user.current_task_id==-1:
                break
            switcher=users[switcher_id]
            if switcher.current_task_id!=-1 and user_id!=switcher_id and user.current_task_id!=switcher.current_task_id and user_id in tasks[switcher.current_task_id].avalible_users and switcher_id in tasks[user.current_task_id].avalible_users:
                user_task=tasks[user.current_task_id]
                switcher_task=tasks[switcher.current_task_id]

                print('at first,user task %d\'s users are:' % user_task.task_id)
                for member_id in user_task.current_avalible_users:
                    print(member_id)

                print('at first,switcher task %d\'s users are:' % switcher_task.task_id)
                for member_id in switcher_task.current_avalible_users:
                    print(member_id)

                #将user移除，添加switcher
                ifremove_user = False

                #抛出ValueError错误
                try:
                    user_task.current_avalible_users.remove(user_id)
                except ValueError:
                    print('we have value error in switching.')
                    print('user_task %d\'s members are'%user_task.task_id)
                    for member_id in user_task.current_avalible_users:
                        print(member_id)
                    print('current user is',user_id)

                if user_id in user_task.current_caching_users:
                    user_task.current_caching_users.remove(user_id)
                    ifremove_user = True

                user_task.current_avalible_users.append(switcher_id)
                if switcher_id in user_task.caching_users:
                    user_task.current_caching_users.append(switcher_id)

                # 将switcher移除，添加user
                ifremove_switcher = False

                # 抛出ValueError错误
                try:
                    switcher_task.current_avalible_users.remove(switcher_id)
                except ValueError:
                    print('we have value error in switching.')
                    print('switcher_task %d\'s members are' % switcher_task.task_id)
                    for member_id in switcher_task.current_avalible_users:
                        print(member_id)
                    print('current user is',user_id)

                if switcher_id in switcher_task.current_caching_users:
                    switcher_task.current_caching_users.remove(switcher_id)
                    ifremove_switcher = True

                switcher_task.current_avalible_users.append(user_id)
                if user_id in switcher_task.caching_users:
                    switcher_task.current_caching_users.append(user_id)

                print('after switching,user task %d\'s users are:'%user_task.task_id)
                for member_id in user_task.current_avalible_users:
                    print(member_id)

                print('after switching,switcher task %d\'s users are:'%switcher_task.task_id)
                for member_id in switcher_task.current_avalible_users:
                    print(member_id)

                #查询交换过的coalition是否已经计算过
                if user_task.ifCoalitionExist(user_task.current_avalible_users)==True and switcher_task.ifCoalitionExist(switcher_task.current_avalible_users)==True:
                    # 将user和switcher复原

                    # 将switcher移除，添加user
                    user_task.current_avalible_users.remove(switcher_id)
                    if switcher_id in user_task.current_caching_users:
                        user_task.current_caching_users.remove(switcher_id)

                    user_task.current_avalible_users.append(user_id)
                    if ifremove_user:
                        user_task.current_caching_users.append(user_id)

                    # 将user移除，添加switcher
                    switcher_task.current_avalible_users.remove(user_id)
                    if user_id in switcher_task.current_caching_users:
                        switcher_task.current_caching_users.remove(user_id)

                    switcher_task.current_avalible_users.append(switcher_id)
                    if ifremove_switcher:
                        switcher_task.current_caching_users.append(switcher_id)

                    print('having calculated,retriving user task %d\'s users are:'%user_task.task_id)
                    for member_id in user_task.current_avalible_users:
                        print(member_id)

                    print('having calculated,retriving switcher task %d\'s users are:'%switcher_task.task_id)
                    for member_id in switcher_task.current_avalible_users:
                        print(member_id)
                    continue

                new_user_task_graph = MC_graph.createMCgraph(user_task, user_task.current_caching_users,
                                                             user_task.current_avalible_users,users)

                try:
                    new_user_flowdict = nx.network_simplex(new_user_task_graph, demand='demand', capacity='capacity',
                                                       weight='weight')
                except nx.NetworkXUnfeasible:
                    print('Error occurs: no flow satisfies all node demands')
                    # 将switcher移除，添加user
                    user_task.current_avalible_users.remove(switcher_id)
                    if switcher_id in user_task.current_caching_users:
                        user_task.current_caching_users.remove(switcher_id)

                    user_task.current_avalible_users.append(user_id)
                    if ifremove_user:
                        user_task.current_caching_users.append(user_id)

                    # 将user移除，添加switcher
                    switcher_task.current_avalible_users.remove(user_id)
                    if user_id in switcher_task.current_caching_users:
                        switcher_task.current_caching_users.remove(user.user_id)

                    switcher_task.current_avalible_users.append(switcher_id)
                    if ifremove_switcher:
                        switcher_task.current_caching_users.append(switcher_id)
                    continue

                new_switcher_task_graph=MC_graph.createMCgraph(switcher_task,switcher_task.current_caching_users,switcher_task.current_avalible_users,users)
                try:
                    new_switcher_flowdict=nx.network_simplex(new_switcher_task_graph, demand='demand', capacity='capacity', weight='weight')
                except nx.NetworkXUnfeasible:
                    print('Error occurs: no flow satisfies all node demands')
                    # 将switcher移除，添加user
                    user_task.current_avalible_users.remove(switcher_id)
                    if switcher_id in user_task.current_caching_users:
                        user_task.current_caching_users.remove(switcher_id)

                    user_task.current_avalible_users.append(user_id)
                    if ifremove_user:
                        user_task.current_caching_users.append(user_id)

                    # 将user移除，添加switcher
                    switcher_task.current_avalible_users.remove(user_id)
                    if user_id in switcher_task.current_caching_users:
                        switcher_task.current_caching_users.remove(user.user_id)

                    switcher_task.current_avalible_users.append(switcher_id)
                    if ifremove_switcher:
                        switcher_task.current_caching_users.append(switcher_id)
                    continue

                #将user和switcher复原
                if new_user_flowdict[0]+new_switcher_flowdict[0] >= user_task.current_flowdict[0]+switcher_task.current_flowdict[0]:
                    print('task %d and task %d have no switching' % (
                    user_task.task_id, switcher_task.task_id))
                    # 将switcher移除，添加user
                    user_task.current_avalible_users.remove(switcher_id)
                    if switcher_id in user_task.current_caching_users:
                        user_task.current_caching_users.remove(switcher_id)

                    user_task.current_avalible_users.append(user_id)
                    if ifremove_user:
                        user_task.current_caching_users.append(user_id)

                    # 将user移除，添加switcher
                    switcher_task.current_avalible_users.remove(user_id)
                    if user_id in switcher_task.current_caching_users:
                        switcher_task.current_caching_users.remove(user.user_id)

                    switcher_task.current_avalible_users.append(switcher_id)
                    if ifremove_switcher:
                        switcher_task.current_caching_users.append(switcher_id)

                    print('no switching, retriving user task %d\'s users are:'% user_task.task_id)
                    for user_id in user_task.current_avalible_users:
                        print(user_id)

                    print('no switching,retriving switcher task %d\'s users are:'% switcher_task.task_id)
                    for switcher_id in switcher_task.current_avalible_users:
                        print(switcher_id)

                else:
                    print('task %d\'s coalition and task %d\'s have changed by switching user %d and user %d' % (user_task.task_id, switcher_task.task_id,user.user_id,switcher.user_id))
                    ifcoalitionchange=True
                    iteration+=1
                    removeUnused(user_task, new_user_flowdict, users)
                    removeUnused(switcher_task, new_switcher_flowdict, users)

    return (ifcoalitionchange,iteration)

def retreating(users,tasks,iteration):
    ifcoalitionchange=False
    for user_id in range(0,len(users)):
        user=users[user_id]
        if user.current_task_id!=-1:
            task=tasks[user.current_task_id]

            ifremove_user = False
            task.current_avalible_users.remove(user.user_id)

            if task.ifCoalitionExist(task.current_avalible_users):
                task.current_avalible_users.append(user.user_id)
                continue

            if user.user_id in task.current_caching_users:
                task.current_caching_users.remove(user.user_id)
                ifremove_user = True

            new_task_graph = MC_graph.createMCgraph(task, task.current_caching_users,
                                                         task.current_avalible_users,users)
            try:
                new_task_flowdict = nx.network_simplex(new_task_graph, demand='demand', capacity='capacity',
                                                   weight='weight')
            except nx.NetworkXUnfeasible:
                print('Error occurs: no flow satisfies all node demands')
                task.current_avalible_users.append(user.user_id)
                if ifremove_user:
                    task.current_caching_users.append(user.user_id)
            else:
                if new_task_flowdict[0]>=task.current_flowdict[0]:
                    task.current_avalible_users.append(user.user_id)
                    if ifremove_user:
                        task.current_caching_users.append(user.user_id)
                else:
                    ifcoalitionchange=True
                    iteration+=1
                    user.current_task_id=-1
                    print('user %d has retreated from task %d' % (
                    user.user_id, task.task_id))
                    removeUnused(task, new_task_flowdict, users)

    return (ifcoalitionchange,iteration)


def removeUnused(task,current_flowdict,users):
    modified_caching_members=[]
    modified_avalible_members=[]
    min_cost, flowdict=current_flowdict
    removed_users=[]

    residual_flowdict=sorted([(u, v) for u in flowdict for v in flowdict[u] if flowdict[u][v] > 0])

   #将没有流量通过的边去掉
    for u,v in residual_flowdict:
        u_id = re.sub('\D','', u)
        v_id = re.sub('\D','', v)
        u_function = u.replace(u_id, '')
        v_function = v.replace(v_id, '')

        '''
        flow_size = flowdict[u][v]
        # 记录每个参与到coalition的user的花费
        if u_function == 'caching' and v_function == 'computing':
            caching_id = int(u_id)
            computing_id = int(v_id)
            users[caching_id].current_cost += task.current_mc_graph[u][v]['caching_user_cost'] * flow_size
            users[computing_id].current_cost += task.current_mc_graph[u][v]['computing_user_cost'] * flow_size
        elif u_function == 'IOTplatform' and v_function == 'computing':
            computing_id = int(v_id)
            users[computing_id].current_cost += task.current_mc_graph[u][v]['computing_user_cost'] * flow_size
        elif u_function == 'computing' and v_function == 'relaying':
            computing_id = int(u_id)
            relaying_id = int(v_id)
            users[computing_id].current_cost += task.current_mc_graph[u][v]['computing_user_cost'] * flow_size
            users[relaying_id].current_cost += task.current_mc_graph[u][v]['relaying_user_cost'] * flow_size
        '''

        if u_id != '':
            user_id=int(u_id)
            if user_id not in modified_avalible_members:
                modified_avalible_members.append(user_id)
                if u_function=='caching'and user_id not in modified_caching_members:
                    modified_caching_members.append(user_id)

        if v_id != '':
            user_id=int(v_id)
            if user_id not in modified_avalible_members:
                modified_avalible_members.append(user_id)
                if v_function=='caching'and user_id not in modified_caching_members:
                    modified_caching_members.append(user_id)

    mc_graph=MC_graph.createMCgraph(task,modified_caching_members, modified_avalible_members,users)
    modified_flowdict=nx.network_simplex(mc_graph, demand='demand', capacity='capacity', weight='weight')

    #记录task当前的coalition状况
    task.current_flowdict = copy.deepcopy(modified_flowdict)
    task.current_mc_graph = copy.deepcopy(mc_graph)

    task.current_caching_users=copy.deepcopy(modified_caching_members)

    for member_id in task.current_avalible_users:
        if member_id in modified_avalible_members:
            users[member_id].current_task_id=task.task_id
        else:
            removed_users.append(member_id)


    for member_id in removed_users:
        users[member_id].current_task_id=-1
        users[member_id].current_cost=0

    task.current_avalible_users=copy.deepcopy(modified_avalible_members)

    #记录每个task已经组过的coalition及其组成情况
    task.record_UserHistory(task.current_avalible_users)
