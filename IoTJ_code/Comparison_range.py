import random as rand
import numpy as np
import sys

sys.setrecursionlimit(1000000000)  # 例如这里设置为一百万

def local_effect(users):
    #local execution
    total_localexecution_energy=0.0
    total_localexecution_time = 0.0
    total_overhead=0.0

    user_num=len(users)

    for i in range(0,user_num):
        total_localexecution_time +=users[i].localexecution_time
        total_localexecution_energy += users[i].localexecution_energy
        total_overhead+=users[i].local_processing_overhead

    return [total_overhead,total_localexecution_time,total_localexecution_energy]

def directToCloud_effect(users):
    total_directTocloud_energy = 0.0
    total_directTocloud_time = 0.0
    total_overhead = 0.0

    user_num = len(users)

    for i in range(0,user_num):
        total_directTocloud_time +=users[i].directTocloud_time
        total_directTocloud_energy += users[i].directTocloud_energy
        total_overhead+=users[i].direct_cloud_execution_overhead

    return [total_overhead,total_directTocloud_time,total_directTocloud_energy]

def decen_reciprocal_effect(users,decen_reciprocalCycles,duration_time):
    total_decen_optimalexecution_time = 0.0
    total_decen_optimalexecution_energy = 0.0
    total_decen_overhead = 0.0

    for cycle in decen_reciprocalCycles:
        cycle_length=len(cycle)
        for i in range(0,cycle_length):
            helperid=cycle[(i+1)%cycle_length]
            userid=cycle[i]

            user=users[userid]

            indexofhelper=user.preference_list.index(helperid)

            total_decen_optimalexecution_time += (user.time_overheads[indexofhelper]+duration_time)
            total_decen_optimalexecution_energy += user.energy_overheads[indexofhelper]
            total_decen_overhead+=(user.overheads[indexofhelper]+ duration_time*user.current_task.weighting_time)

            if i==cycle_length-1:
                break

    return [total_decen_overhead,total_decen_optimalexecution_time,total_decen_optimalexecution_energy]

def cen_reciprocal_effect(users,cen_reciprocalCycles,duration_time):
    total_cen_optimalexecution_time = 0.0
    total_cen_optimalexecution_energy = 0.0
    total_cen_overhead = 0.0

    for cycle in cen_reciprocalCycles:
        cycle_length=len(cycle)
        for i in range(0,cycle_length):
            helperid=cycle[(i+1)%cycle_length]
            userid=cycle[i]

            user=users[userid]

            indexofhelper=user.preference_list.index(helperid)

            user_probing_result=user.reporting_result()

            total_cen_optimalexecution_time += (user.time_overheads[indexofhelper]+user_probing_result[0]+duration_time)
            total_cen_optimalexecution_energy += (user.energy_overheads[indexofhelper]+user_probing_result[1])

            user_probing_overhead=(user_probing_result[0]+duration_time)*user.current_task.weighting_time + user_probing_result[1]* user.current_task.weighting_energy

            total_cen_overhead+=(user.overheads[indexofhelper]+user_probing_overhead)

            if i==cycle_length-1:
                break


    return [total_cen_overhead,total_cen_optimalexecution_time,total_cen_optimalexecution_energy]

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

def greedy_reciprocal_effect(users):
    total_greedyreciprocal_time = 0.0
    total_greedyreciprocal_energy = 0.0
    total_overhead=0.0

    user_num = len(users)
    unmatched_usersid = [i for i in range(0, user_num)]
    user_helpers = []
    local_overheads = []

    for user in users:
        local_overheads.append(user.local_processing_overhead)

    quicksort(local_overheads, unmatched_usersid, 0, user_num - 1)
    print('根据overheads排序结果：', unmatched_usersid)


    for i in unmatched_usersid:
        if i not in user_helpers:
            for j in users[i].preference_list:
                if j not in user_helpers:

                    if i == j:
                        user_helpers.append(j)
                        indexofhelper = users[i].preference_list.index(j)

                        total_greedyreciprocal_time+=users[i].time_overheads[indexofhelper]
                        total_greedyreciprocal_energy+=users[i].energy_overheads[indexofhelper]
                        total_overhead+=users[i].overheads[indexofhelper]

                        break
                    else:
                        #'''
                        index_of_j = users[i].preference_list.index(j)
                        overhead_of_i = users[i].overheads[index_of_j]
                        time_overhead_of_i=users[i].time_overheads[index_of_j]
                        energy_overhead_of_i=users[i].energy_overheads[index_of_j]

                        index_of_i = users[j].preference_list.index(i)
                        overhead_of_j = users[j].overheads[index_of_i]
                        time_overhead_of_j = users[j].time_overheads[index_of_i]
                        energy_overhead_of_j = users[j].energy_overheads[index_of_i]

                        user_helpers.append(i)
                        user_helpers.append(j)

                        total_greedyreciprocal_time += (time_overhead_of_i + time_overhead_of_j)
                        total_greedyreciprocal_energy += (energy_overhead_of_i + energy_overhead_of_j)
                        total_overhead += (overhead_of_i + overhead_of_j)

                        break
                        #'''

                        '''
                        user=users[i];helper=users[j]
                        user_itself_overhead=user.overheads[user.preference_list.index(i)]
                        helper_itself_overhead = helper.overheads[helper.preference_list.index(j)]

                        index_of_j = users[i].preference_list.index(j)
                        overhead_of_i = users[i].overheads[index_of_j]
                        time_overhead_of_i = users[i].time_overheads[index_of_j]
                        energy_overhead_of_i = users[i].energy_overheads[index_of_j]

                        index_of_i = users[j].preference_list.index(i)
                        overhead_of_j = users[j].overheads[index_of_i]
                        time_overhead_of_j = users[j].time_overheads[index_of_i]
                        energy_overhead_of_j = users[j].energy_overheads[index_of_i]



                        if overhead_of_i < user_itself_overhead and overhead_of_j < helper_itself_overhead:
                            total_greedyreciprocal_time += (time_overhead_of_i + time_overhead_of_j)
                            total_greedyreciprocal_energy += (energy_overhead_of_i + energy_overhead_of_j)
                            total_overhead += (overhead_of_i + overhead_of_j)
                            user_helpers.append(i)
                            user_helpers.append(j)
                            break
                        '''

    return [total_overhead,total_greedyreciprocal_time,total_greedyreciprocal_energy]

def randomReciprocity_effect(users):
    total_time_overhead=0
    total_energy_overhead=0
    total_overhead=0

    user_num = len(users)
    unmatched_usersid = [i for i in range(0, user_num)]
    user_helpers = []
    rand.shuffle(unmatched_usersid)
    unmatched_helpers = [i for i in range(0, user_num)]
    rand.shuffle(unmatched_helpers)

    for i in unmatched_usersid:
        if i not in user_helpers:
            for j in unmatched_helpers:
                if j not in user_helpers and j in users[i].preference_list:

                    if i == j:
                        user_helpers.append(j)
                        indexofhelper = users[i].preference_list.index(j)
                        total_time_overhead += users[i].time_overheads[indexofhelper]
                        total_energy_overhead += users[i].energy_overheads[indexofhelper]
                        total_overhead += users[i].overheads[indexofhelper]
                        break
                    else:
                        #'''
                        index_of_j = users[i].preference_list.index(j)
                        overhead_of_i = users[i].overheads[index_of_j]
                        time_overhead_of_i = users[i].time_overheads[index_of_j]
                        energy_overhead_of_i = users[i].energy_overheads[index_of_j]

                        index_of_i = users[j].preference_list.index(i)
                        overhead_of_j = users[j].overheads[index_of_i]
                        time_overhead_of_j = users[j].time_overheads[index_of_i]
                        energy_overhead_of_j = users[j].energy_overheads[index_of_i]

                        user_helpers.append(i)
                        user_helpers.append(j)
                        total_time_overhead += (time_overhead_of_i + time_overhead_of_j)
                        total_energy_overhead += (energy_overhead_of_i + energy_overhead_of_j)
                        total_overhead += (overhead_of_i + overhead_of_j)
                        break
                        #'''

                        '''
                        user=users[i];helper=users[j]
                        user_itself_overhead=user.overheads[user.preference_list.index(i)]
                        helper_itself_overhead = helper.overheads[helper.preference_list.index(j)]

                        index_of_j = users[i].preference_list.index(j)
                        overhead_of_i = users[i].overheads[index_of_j]
                        time_overhead_of_i = users[i].time_overheads[index_of_j]
                        energy_overhead_of_i = users[i].energy_overheads[index_of_j]

                        index_of_i = users[j].preference_list.index(i)
                        overhead_of_j = users[j].overheads[index_of_i]
                        time_overhead_of_j = users[j].time_overheads[index_of_i]
                        energy_overhead_of_j = users[j].energy_overheads[index_of_i]



                        if overhead_of_i < user_itself_overhead and overhead_of_j < helper_itself_overhead:
                            total_time_overhead += (time_overhead_of_i + time_overhead_of_j)
                            total_energy_overhead += (energy_overhead_of_i + energy_overhead_of_j)
                            total_overhead += (overhead_of_i + overhead_of_j)
                            user_helpers.append(i)
                            user_helpers.append(j)
                            break
                        '''

    return [total_overhead,total_time_overhead,total_energy_overhead]










