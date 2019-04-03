#coding:utf-8
import random as rand
import time

def centralizedAlgorithm(users,user_num):
    time_start=time.time()
    total_signal_overhead = 0

    reciprocalCycles = [] #所有的cycle集合
    t=0
    leftPlayers=[i for i in range(0,user_num)] #每循环一次剩下的没组成cycle的player
    while len(leftPlayers)>0:
        print('iteration is',t)
        current_iteration_players = [i for i in leftPlayers] #每次循环开始之前的所有没进入cycle的player
        unvisited=[i for i in current_iteration_players] #本次循环还没访问的player
        visited=[] #本次循环已经访问的player集合

        for i in leftPlayers:
            for j in users[i].preference_list:
                if j in leftPlayers:
                    users[i].most_preferred_helper_id =j
                    break

        while len(unvisited)>0:
            current_path=[]
            user_id=rand.choice(unvisited)
            current_path.append(user_id)
            flag=0
            while flag==0:
                t = t + 1
                current_user_id=users[user_id].most_preferred_helper_id
                if current_user_id in visited:
                    for i in current_path:
                        if i not in visited:
                           visited.append(i)
                    for i in visited:
                        if i in unvisited:
                           unvisited.remove(i)
                    flag=1
                elif current_user_id in current_path:
                    reciprocalcycle=[i for i in current_path[current_path.index(current_user_id):current_path.index(user_id)+1]]
                    reciprocalCycles.append(reciprocalcycle)
                    print('reciprocalcycle is',reciprocalcycle)
                    for i in reciprocalcycle:
                        if i in leftPlayers:
                           leftPlayers.remove(i)
                    for i in current_path:
                        if i not in visited:
                           visited.append(i)
                    for i in visited:
                        if i in unvisited:
                            unvisited.remove(i)
                    flag = 1
                else:
                    current_path.append(current_user_id)
                    user_id=current_user_id

    time_end=time.time()
    duration_time=(time_end-time_start)   #单位 s

    for user in users:
        total_signal_overhead+=len(user.preference_list)

    for cycle in reciprocalCycles:
        total_signal_overhead+=len(cycle)

    return [reciprocalCycles,t,duration_time,total_signal_overhead]

