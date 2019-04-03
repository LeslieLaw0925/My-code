import random as rand
import numpy as np

def local_effect(users):
    #local execution
    total_localexecution_energy=0.0
    total_localexecution_time = 0.0
    total_overhead=0.0

    for user in users:
        #total_localexecution_energy += user.localexecution_energy
        #total_localexecution_time +=user.localexecution_time
        total_overhead += user.local_processing_overhead

    return total_overhead

def directToCloud_effect(users):
    total_directTocloud_energy = 0.0
    total_directTocloud_time = 0.0
    total_overhead = 0.0

    for user in users:
        #total_directTocloud_energy += user.directTocloud_energy
        #total_directTocloud_time +=user.directTocloud_time
        total_overhead += (user.current_task.weighting_time * user.directTocloud_time + user.current_task.weighting_energy * user.directTocloud_energy)

    return total_overhead

def reciprocal_effect(users,cen_reciprocalCycles):
    total_optimalexecution_time = 0.0
    total_optimalexecution_energy = 0.0
    total_overhead=0.0

    for cycle in cen_reciprocalCycles:
        cycle_length=len(cycle)
        for i in range(0,cycle_length):
            helperid=cycle[(i+1)%cycle_length]
            userid=cycle[i]

            user=users[userid]

            indexofhelper=user.preference_list.index(helperid)
            strategyofhelper=user.strategylist[indexofhelper]
            #total_optimalexecution_energy += user.energy_overheads[indexofhelper]
            #total_optimalexecution_time += user.time_overheads[indexofhelper]
            total_overhead += user.overheads[indexofhelper]

            if strategyofhelper==1:
                print('user %d\'s helper user %d takes local execution strategy' % (userid,helperid))
            elif strategyofhelper==2:
                print('user %d\'s helper user %d takes D2D offloaded execution strategy' % (userid, helperid))
            elif strategyofhelper==3:
                print('user %d\'s helper user %d takes direct cloud offloaded execution strategy' % (userid, helperid))
            else:
                print('user %d\'s helper user %d takes D2D-Assisted cloud offloaded execution strategy' % (userid, helperid))

            if i==cycle_length-1:
                break

    return total_overhead

def quicksort(overheads,unmatched_usersid,low,high):
    if low<high:
        quicksort(overheads,unmatched_usersid,low,partition(overheads,unmatched_usersid,low,high)-1)
        quicksort(overheads,unmatched_usersid,partition(overheads,unmatched_usersid,low,high)+1,high)

def partition(overheads,unmatched_usersid,low,high):
    i = low;j = high;key = overheads[i]
    while i < j:
        while overheads[j] >= key and i < j:
            j -= 1
        unmatched_usersid[i], unmatched_usersid[j] = unmatched_usersid[j], unmatched_usersid[i]
        overheads[i], overheads[j] = overheads[j], overheads[i]

        while overheads[i]<= key and i < j:
            i += 1
        unmatched_usersid[i], unmatched_usersid[j] = unmatched_usersid[j], unmatched_usersid[i]
        overheads[i], overheads[j] = overheads[j], overheads[i]
    return i

def greedy_effect_overhead(users):
    total_overhead=0

    user_num=len(users)
    unmatched_usersid=[i for i in range(0,user_num)]
    user_helpers=[]
    overheads=[]

    for user in users:
        total_overheads=0
        for overhead in user.overheads:
            total_overheads+=overhead
        overheads.append(total_overheads/len(user.overheads))

    print('用户的第一个overheads列表为：',overheads)

    quicksort(overheads,unmatched_usersid,0,user_num-1)
    print('根据overheads排序结果：',unmatched_usersid)

    for i in unmatched_usersid:
        for j in users[i].preference_list:
            if j not in user_helpers:
                user_helpers.append(j)
                indexofhelper = users[i].preference_list.index(j)
                try:
                    strategyofhelper = users[i].strategylist[indexofhelper]
                except IndexError:
                    print('user num is:',user_num)

                total_overhead += users[i].overheads[indexofhelper]

                if strategyofhelper == 1:
                    print('user %d\'s helper user %d takes local execution strategy' % (i, j))
                elif strategyofhelper == 2:
                    print('user %d\'s helper user %d takes D2D offloaded execution strategy' % (i, j))
                elif strategyofhelper == 3:
                    print('user %d\'s helper user %d takes direct cloud offloaded execution strategy' % (i, j))
                else:
                    print('user %d\'s helper user %d takes D2D-Assisted cloud offloaded execution strategy' % (i, j))

                break

    print('相应的helpers结果：', user_helpers)

    return total_overhead

def greedy_effect_gain(users):
    total_greedy_time=0.0
    total_greed_energy=0.0

    user_num=len(users)
    unmatched_usersid=[i for i in range(0,user_num)]
    user_helpers=[]
    overheads=[]

    for user in users:
        total_overheads=0
        for overhead in user.overheads:
            total_overheads+=overhead
        overheads.append(total_overheads/user_num)

    print('用户的第一个overheads列表为：',overheads)

    quicksort(overheads,unmatched_usersid,0,user_num-1)
    print('根据overheads排序结果：',unmatched_usersid)

    for i in unmatched_usersid:
        if i not in user_helpers:
            for j in users[i].preference_list:
                if j not in user_helpers:
                    indexofhelper = users[i].preference_list.index(j)
                    user_helpers.append(j)
                    if i==j:
                       if i < user_num / 2:
                           total_greedy_time += users[i].time_overheads[indexofhelper]
                       else:
                           total_greed_energy += users[i].energy_overheads[indexofhelper]


                    else:
                        indexofhelper_j=users[j].preference_list.index(i)
                        if i < user_num / 2:
                            total_greedy_time += users[i].time_overheads[indexofhelper]
                        else:
                            total_greed_energy += users[i].energy_overheads[indexofhelper]

                        if j < user_num / 2:
                            total_greedy_time += users[i].time_overheads[indexofhelper_j]
                        else:
                            total_greed_energy += users[i].energy_overheads[indexofhelper_j]

                    break


    print('相应的helpers结果：', user_helpers)

    return [total_greedy_time,total_greed_energy]


def random_effect(users):
    total_random_time = 0.0
    total_random_energy = 0.0
    total_overhead=0.0
    strategyofhelper=None

    user_num = len(users)
    user_helpers = []
    unmatched_usersid = [i for i in range(0, user_num)]

    for i in unmatched_usersid:
        helperid=rand.choice(unmatched_usersid)
        while helperid in user_helpers:
            helperid = rand.choice(unmatched_usersid)

        user_helpers.append(helperid)

        if helperid==users[i].user_id:
            strategyofhelper=rand.choice([1,3])
        else:
            strategyofhelper = rand.choice([2, 4])

        if strategyofhelper == 1:
            print('user %d\'s helper user %d takes local execution strategy' % (i, helperid))
            #total_random_time += users[i].localexecution_time
            #total_random_energy += users[i].localexecution_energy
            total_overhead += users[i].local_processing_overhead

        elif strategyofhelper == 2:
            print('user %d\'s helper user %d takes D2D offloaded execution strategy' % (i, helperid))
            results=users[i].D2D_offloaded_execution(users[helperid])
            #total_random_time +=results[1]
            #total_random_energy += results[2]

            total_overhead += results[0]

        elif strategyofhelper == 3:
            print('user %d\'s helper user %d takes direct cloud offloaded execution strategy' % (i, helperid))
            results = users[i].Direct_cloud_execution()
            #total_random_time += users[i].directTocloud_time
            #total_random_energy += users[i].directTocloud_energy
            total_overhead += results[0]

        else:
            print('user %d\'s helper user %d takes D2D-Assisted cloud offloaded execution strategy' % (i, helperid))
            results = users[i].D2D_Assisted_cloud_execution(users[helperid])
            #total_random_time += results[1]
            #total_random_energy += results[2]
            total_overhead += results[0]

    print('相应的helpers结果：', user_helpers)
    return total_overhead

def simpleReciprocity_effect(users):
    user_num=len(users)
    unselected_userids=[i for i in range(0,user_num)]

    total_time_overhead=0
    total_energy_overhead=0
    total_overhead=0.0

    while len(unselected_userids)>0:
        current_user=users[unselected_userids[0]]
        current_local_overhead=current_user.local_processing_overhead
        del unselected_userids[0]
        selected_flag=0
        for i in unselected_userids:
            helper=users[i]

            current_d2d_results=current_user.D2D_offloaded_execution(helper)
            helper_d2d_results=helper.D2D_offloaded_execution(current_user)

            current_d2dToCloud_results=current_user.D2D_Assisted_cloud_execution(helper)
            helper_d2dToCloud_results=helper.D2D_Assisted_cloud_execution(current_user)


            user_d2d_energy=current_d2d_results[3]
            helper_d2d_energy=helper_d2d_results[3]

            user_d2dToCloud_energy=current_d2dToCloud_results[3]
            helper_d2dToCloud_energy=helper_d2dToCloud_results[3]


            if user_d2d_energy < current_local_overhead and helper_d2d_energy < helper.local_processing_overhead: # 2+2
                selected_flag = 1
                #total_time_overhead += (current_d2d_results[1] + helper_d2d_results[1])
                #total_energy_overhead += (current_d2d_results[2] + helper_d2d_results[2])
                total_overhead+=(current_d2d_results[0]+helper_d2d_results[0])
                unselected_userids.remove(i)
                break
            elif user_d2d_energy < current_local_overhead and helper_d2dToCloud_energy < helper.local_processing_overhead:  # 2+4
                selected_flag = 1
                #total_time_overhead += (current_d2d_results[1] + helper_d2dToCloud_results[1])
                #total_energy_overhead += (current_d2d_results[2] + helper_d2dToCloud_results[2])
                total_overhead += (current_d2d_results[0] + helper_d2dToCloud_results[0])
                unselected_userids.remove(i)
                break
            elif user_d2dToCloud_energy < current_local_overhead and helper_d2dToCloud_energy < helper.local_processing_overhead:  # 4+4
                selected_flag = 1
                #total_time_overhead += (current_d2dToCloud_results[1] + helper_d2dToCloud_results[1])
                #total_energy_overhead += (current_d2dToCloud_results[2] + helper_d2dToCloud_results[2])
                total_overhead += (current_d2dToCloud_results[0] + helper_d2dToCloud_results[0])
                unselected_userids.remove(i)
                break
            elif user_d2dToCloud_energy < current_local_overhead and helper_d2d_energy < helper.local_processing_overhead:  # 4+2
                selected_flag = 1
                #total_time_overhead += (current_d2dToCloud_results[1] + helper_d2d_results[1])
                #total_energy_overhead += (current_d2dToCloud_results[2] + helper_d2d_results[2])
                total_overhead += (current_d2dToCloud_results[0] + helper_d2d_results[0])
                unselected_userids.remove(i)
                break

        if selected_flag == 0:
            print('user %d 本地执行' % current_user.user_id)
            #total_time_overhead += current_user.localexecution_time
            #total_energy_overhead += current_user.localexecution_energy
            total_overhead+=current_user.local_processing_overhead

    return total_overhead











