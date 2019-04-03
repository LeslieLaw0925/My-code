#coding:utf-8
import Quicksort

def findPreferenceList(users,user_num):
    for j in range(0,user_num):
        for i in users[j].preference_list:
            if i==j:
                local_overhead=users[j].LocalExecution()
                direct_to_cloud_overhead=users[j].Direct_cloud_execution()
                if local_overhead[0]>direct_to_cloud_overhead[0]:
                    users[j].strategylist.append(3)
                    users[j].overheads.append(direct_to_cloud_overhead[0])
                    users[j].time_overheads.append(direct_to_cloud_overhead[1])
                    users[j].energy_overheads.append(direct_to_cloud_overhead[2])
                else:
                    users[j].strategylist.append(1)
                    users[j].overheads.append(local_overhead[0])
                    users[j].time_overheads.append(local_overhead[1])
                    users[j].energy_overheads.append(local_overhead[2])


            else:
                d2d_offloaded_overhead=users[j].D2D_offloaded_execution(users[i])
                d2d_assisted_cloud_offloaded_overhead=users[j].D2D_Assisted_cloud_execution(users[i])
                if d2d_assisted_cloud_offloaded_overhead[0]>d2d_offloaded_overhead[0]:
                    users[j].strategylist.append(2)
                    users[j].overheads.append(d2d_offloaded_overhead[0])
                    users[j].time_overheads.append(d2d_offloaded_overhead[1])
                    users[j].energy_overheads.append(d2d_offloaded_overhead[2])
                else:
                    users[j].strategylist.append(4)
                    users[j].overheads.append(d2d_assisted_cloud_offloaded_overhead[0])
                    users[j].time_overheads.append(d2d_assisted_cloud_offloaded_overhead[1])
                    users[j].energy_overheads.append(d2d_assisted_cloud_offloaded_overhead[2])

        Quicksort.quicksort(users[j].preference_list, 0, len(users[j].preference_list)-1, users[j].overheads,users[j].strategylist,users[j].time_overheads,users[j].energy_overheads)

        print('sorted preference list of user %d is' % j)
        print(users[j].preference_list)
        print(users[j].strategylist)
        print(users[j].overheads)
        print(users[j].time_overheads)
        print(users[j].energy_overheads)
        print('\n')





