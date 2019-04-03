#coding:utf-8
import CalculatePreferencelists
import DecentralizedAlgorithm
import CentralizedAlgorithm
from User import User
from ReciprocalGraph import ReciprocalGraph
from Task import Task
import Comparison_range

cen_reciprocalCycles=None
decen_reciprocalCycles=None
user_num=10
users=[]
reciprocalGraph=ReciprocalGraph(user_num)
iteration_num=1000

for i in range(0,user_num):
    user=User(i)

    users.append(user)

for i in range(0,iteration_num):
    for user in users:
        user.initialize()
        user.setPreferrencelist(user_num)
        task = Task()
        user.setCurrentTask(task)

    CalculatePreferencelists.findPreferenceList(users,user_num)

    #执行centralized算法
    print('Result of centralized algorithm：')
    cen_reciprocalCycles=CentralizedAlgorithm.centralizedAlgorithm(users,user_num)
    print(cen_reciprocalCycles)

    greedyresults=Comparison_range.greedy_reciprocal_effect(users)



    #Comparison.greedy_effect(users)





