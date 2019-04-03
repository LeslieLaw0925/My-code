import mwmatching
import random as rand

def cen_reciprocal_effect(users,cen_reciprocalCycles):
    total_overhead = 0.0
    beneficial_user_num=0
    modes=[0 for i in range(0,4)]

    for cycle in cen_reciprocalCycles:
        cycle_length = len(cycle)
        if cycle_length!=1:
            beneficial_user_num+=cycle_length

        for i in range(0, cycle_length):
            helperid = cycle[(i + 1) % cycle_length]
            userid = cycle[i]

            user = users[userid]

            indexofhelper = user.preference_list.index(helperid)
            mode=user.strategylist[indexofhelper]
            if mode==1:
                modes[0]+=1
            elif mode==2:
                modes[1]+=1
            elif mode==3:
                modes[2]+=1
            elif mode == 4:
                modes[3]+=1

            total_overhead += user.overheads[indexofhelper]

            if i == cycle_length - 1:
                break

    return [total_overhead,beneficial_user_num,modes]

def execute_mwmatching(users):
    edges = []
    usernum = len(users)
    beneficial_usernum=0
    modes = [0 for i in range(0, 4)]

    for user in users:
        user_id = user.user_id
        for helper_id in user.preference_list:
            helper = users[helper_id]
            if user_id != helper_id:
                overhead_of_user = user.overheads[user.preference_list.index(helper_id)]
                overhead_of_helper = helper.overheads[helper.preference_list.index(user_id)]
                weight = -1 * (overhead_of_user + overhead_of_helper)
                edge1 = (user_id, helper_id, weight)
                edge2 = (helper_id, user_id, weight)
                if edge1 not in edges and edge2 not in edges:
                    edges.append(edge1)

    last_user = users[usernum - 1]
    overhead_of_lastuser = last_user.overheads[last_user.preference_list.index(usernum - 1)]
    edges.append((usernum - 1, usernum, overhead_of_lastuser))

    print('All the edges are', edges)
    mate = mwmatching.maxWeightMatching(edges, True)

    print('the result of mate is', mate)

    total_mwmatching_overhead = 0

    selected_users = []

    for user_id in range(0, usernum):
        matching_id = mate[user_id]
        user = users[user_id]

        if matching_id == -1 or matching_id == user_id + 1:
            total_mwmatching_overhead += user.overheads[user.preference_list.index(user_id)]
            selected_users.append(user_id)

            mode = user.strategylist[user.preference_list.index(user_id)]
            if mode == 1:
                modes[0] += 1
            elif mode == 3:
                modes[2] += 1

        else:
            if user_id not in selected_users and matching_id not in selected_users:
                helper = users[matching_id]

                overhead_of_user = user.overheads[user.preference_list.index(matching_id)]
                overhead_of_helper = helper.overheads[helper.preference_list.index(user_id)]

                total_mwmatching_overhead += (overhead_of_user + overhead_of_helper)

                selected_users.append(user_id)
                selected_users.append(matching_id)

                mode = user.strategylist[user.preference_list.index(matching_id)]
                if mode == 1:
                    modes[0] += 1
                elif mode == 2:
                    modes[1] += 1
                elif mode == 3:
                    modes[2] += 1
                elif mode == 4:
                    modes[3] += 1

                mode = helper.strategylist[helper.preference_list.index(user_id)]
                if mode == 1:
                    modes[0] += 1
                elif mode == 2:
                    modes[1] += 1
                elif mode == 3:
                    modes[2] += 1
                elif mode == 4:
                    modes[3] += 1

                if user.preference_list.index(matching_id) < user.preference_list.index(user_id):
                    beneficial_usernum+=1
                if helper.preference_list.index(user_id) < helper.preference_list.index(matching_id):
                    beneficial_usernum +=1

    return [total_mwmatching_overhead, beneficial_usernum,modes]

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
    total_greedyreciprocal_overhead=0.0
    beneficial_usernum=0
    modes=[0 for i in range(0,4)]

    user_num = len(users)
    unmatched_usersid = [i for i in range(0, user_num)]
    user_helpers = []
    local_overheads = []

    unmatched_helpers = [i for i in range(0, user_num)]
    rand.shuffle(unmatched_helpers)

    for user in users:
        user_itself_overhead = user.overheads[user.preference_list.index(user.user_id)]
        local_overheads.append(user_itself_overhead)


    quicksort(local_overheads, unmatched_usersid, 0, user_num - 1)
    print('根据overheads排序结果：', unmatched_usersid)

    for i in unmatched_usersid:
        if i not in user_helpers:
            for j in users[i].preference_list:
                if j not in user_helpers:

                    if i==j:
                        user_helpers.append(j)
                        indexofhelper = users[i].preference_list.index(j)
                        total_greedyreciprocal_overhead += users[i].overheads[indexofhelper]

                        mode = users[i].strategylist[indexofhelper]
                        if mode == 1:
                            modes[0] += 1
                        elif mode == 3:
                            modes[2] += 1

                        break
                    else:
                        index_of_j = users[i].preference_list.index(j)
                        overhead_of_i = users[i].overheads[index_of_j]

                        index_of_i = users[j].preference_list.index(i)
                        overhead_of_j = users[j].overheads[index_of_i]

                        user=users[i];helper=users[j]
                        user_itself_overhead=user.overheads[user.preference_list.index(i)]

                        helper_itself_overhead=helper.overheads[helper.preference_list.index(j)]

                        if overhead_of_i < user_itself_overhead and overhead_of_j < helper_itself_overhead:
                            user_helpers.append(i)
                            user_helpers.append(j)
                            total_greedyreciprocal_overhead += (overhead_of_i + overhead_of_j)
                            beneficial_usernum+=2

                            mode = user.strategylist[user.preference_list.index(j)]
                            if mode == 1:
                                modes[0] += 1
                            elif mode == 2:
                                modes[1] += 1
                            elif mode == 3:
                                modes[2] += 1
                            elif mode == 4:
                                modes[3] += 1

                            mode = helper.strategylist[helper.preference_list.index(i)]
                            if mode == 1:
                                modes[0] += 1
                            elif mode == 2:
                                modes[1] += 1
                            elif mode == 3:
                                modes[2] += 1
                            elif mode == 4:
                                modes[3] += 1

                            break

    return [total_greedyreciprocal_overhead,beneficial_usernum,modes]

def randomreciprocal_effect(users):
    total_randomreciprocal_overhead=0
    beneficial_usernum=0
    modes=[0 for i in range(0,4)]

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
                        total_randomreciprocal_overhead += users[i].overheads[indexofhelper]

                        mode = users[i].strategylist[indexofhelper]
                        if mode == 1:
                            modes[0] += 1
                        elif mode == 3:
                            modes[2] += 1

                        break
                    else:
                        index_of_j = users[i].preference_list.index(j)
                        overhead_of_i = users[i].overheads[index_of_j]

                        index_of_i = users[j].preference_list.index(i)
                        overhead_of_j = users[j].overheads[index_of_i]

                        user=users[i];helper=users[j]
                        user_itself_overhead=user.overheads[user.preference_list.index(i)]

                        helper_itself_overhead=helper.overheads[helper.preference_list.index(j)]

                        if overhead_of_i < user_itself_overhead and overhead_of_j < helper_itself_overhead:
                            user_helpers.append(i)
                            user_helpers.append(j)
                            beneficial_usernum+=2
                            total_randomreciprocal_overhead += (overhead_of_i + overhead_of_j)

                            mode = user.strategylist[user.preference_list.index(j)]
                            if mode == 1:
                                modes[0] += 1
                            elif mode == 2:
                                modes[1] += 1
                            elif mode == 3:
                                modes[2] += 1
                            elif mode == 4:
                                modes[3] += 1

                            mode = helper.strategylist[helper.preference_list.index(i)]
                            if mode == 1:
                                modes[0] += 1
                            elif mode == 2:
                                modes[1] += 1
                            elif mode == 3:
                                modes[2] += 1
                            elif mode == 4:
                                modes[3] += 1

                            break

    return [total_randomreciprocal_overhead,beneficial_usernum,modes]