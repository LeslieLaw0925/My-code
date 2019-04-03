#coding:utf-8
import random as rand
import time

#记录已走过的user

def decentralizedAlgorithm(users,user_num):
    duration_time=0
    total_signal_overhead=0

    probing_message_size=1.5*1024 * 8 #1KB

    t=0
    reciprocalCycles = []
    MESG = []
    ZeroFlags = [i for i in range(0,user_num)]
    global user,most_preferred_helper_id

    while len(ZeroFlags)>0:
        '''
        #所有flag=0的device而且preference list大于1的广播包竞争reciprocal cycle的探索权
        for i in ZeroFlags:
            if len(users[i].preference_list)>1:
                total_signal_overhead += 1
        '''
        user = users[rand.choice(ZeroFlags)]

        #user 竞争成功，广播一个包告知其他device
        total_signal_overhead+=1

        MESG.append(user.user_id)
        for i in user.preference_list:
            t += 1
            # 当前user把MESG传到当前最优helper
            if i!=user.user_id:
                total_signal_overhead += 1
                duration_time+=(probing_message_size/user.transmission_datarate(users[i])) #单位：秒s

            if users[i].flag == 0:
                most_preferred_helper_id = i
                break

        while most_preferred_helper_id not in MESG:
            t += 1
            user = users[most_preferred_helper_id]
            MESG.append(most_preferred_helper_id)
            for i in user.preference_list:

                # 当前user把MESG传到当前最优helper
                if i != user.user_id:
                    total_signal_overhead += 1
                    duration_time += (probing_message_size / user.transmission_datarate(users[i]))  # 单位：秒s

                if users[i].flag == 0:
                    most_preferred_helper_id = i
                    break


        if most_preferred_helper_id in MESG:
            reciprocalCycles.append([i for i in MESG[MESG.index(most_preferred_helper_id):MESG.index(user.user_id)+1]])
            #当前device把已经发现的reciprocal cycle告诉其他所有的devices
            total_signal_overhead += 1
            for i in MESG[MESG.index(most_preferred_helper_id):MESG.index(user.user_id)+1]:
                users[i].flag=1
                if i in ZeroFlags:
                   ZeroFlags.remove(i)

        del MESG[:]

    return [reciprocalCycles,t,duration_time,total_signal_overhead]


