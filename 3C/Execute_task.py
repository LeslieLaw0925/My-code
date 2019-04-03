from User import User
from Content import Content
from Task import Task
import math
import CoalitionFormation
import Comparison
import datetime
import random as rand

users=[]
contents=[]
tasks=[]

user_num=100
task_nums=[10,15,20,25,30,35]

user_range=500

def execute():
    for i in range(0, user_num):
        user = User(i)
        user.initialize()
        users.append(user)

    for user in users:
        user.setAvalibleCooperators(user_range, users)

    for i in range(0, Content.content_num):
        content = Content(i)
        contents.append(content)

    result_file = open('Experiment/task_num.docx', 'w')

    #计算不同任务数目在系统中的表现

    for i in range(0,len(task_nums)):
        task_num=task_nums[i]
        joined_users = []

        if i == 0:
            for i in range(0, task_nums[i]):
                task = Task(contents, i)
                task.setAvalibaleUsers(users)
                task.setCachingUsers(users)
                tasks.append(task)
        else:
            for i in range(task_nums[i - 1], task_nums[i]):
                task = Task(contents, i)
                task.setAvalibaleUsers(users)
                task.setCachingUsers(users)
                tasks.append(task)


        for user in users:
            user.avalibleTasks.clear()
            user.current_task_id=-1
            for task in tasks:
                distance = math.sqrt(
                    math.pow((task.x_axis - task.x_axis), 2) + math.pow((task.y_axis - task.y_axis), 2))
                if distance<Task.task_range:
                    user.avalibleTasks.append(task.task_id)


        for task in tasks:
            task.initilize()
            task.Non_cooperation_initialize(joined_users,users)

            print('task %d\'s mc_graph is'% task.task_id)
            print(task.current_mc_graph.edge)
            print('task %d\'s min cost flow dict is' % task.task_id)
            print(task.current_flowdict)

            print('task %d\'s current avalible members are' % task.task_id)
            print(task.current_avalible_users)
            print('task %d\'s current caching members are' % task.task_id)
            print(task.current_caching_users)
            for user_id in task.current_avalible_users:
                print('the cost of user %d of task %d is: %d' % (user_id, task.task_id, users[user_id].current_cost))

            print('\n')

        initial_totalcost_CF=0
        for task in tasks:
            initial_totalcost_CF+=task.current_flowdict[0]

        starttime_CF = datetime.datetime.now()
        CF_result=CoalitionFormation.coalitionFormation(users,tasks)
        totalcost_CF=CF_result[0]
        CF_participated_usernum=CF_result[1]
        iteration_number=CF_result[2]

        endtime_CF = datetime.datetime.now()


        for task in tasks:
            print('task %d\'s mc_graph is' % task.task_id)
            print(task.current_mc_graph.edge)
            print('task %d\'s min cost flow dict is' % task.task_id)
            print(task.current_flowdict)
            print('task %d\'s current avalible members are' % task.task_id)
            print(task.current_avalible_users)
            print('task %d\'s current caching members are' % task.task_id)
            print(task.current_caching_users)
            print('\n')


        totalcost_NC=Comparison.Non_Cooperation(users,tasks)
        totalcost_NCG=Comparison.Non_Cooperation_greedy(users,tasks)

        '''
        BruteForce_starttime = datetime.datetime.now()
        BruteForce_cost=Comparison.BruteForce(tasks,users)
        BruteForce_endtime = datetime.datetime.now()
    
        result_file.write('task num is %d\n' % task_num)
        result_file.write('BruteForce\'s total cost is %d\n' % BruteForce_cost)
        result_file.write('Compared to CF, approximation of BruteForce improves is %f%%\n' % (totalcost_CF/BruteForce_cost*100))
        result_file.write('Running time of CoalitionFormation is %d second(s)\n' % (endtime_CF - starttime_CF).seconds)
        result_file.write ('Running time of BruteForce is %d second(s)\n'%(BruteForce_endtime - BruteForce_starttime).seconds)
        result_file.write('\n\n')
        '''
        for user in users:
            user.current_task_id=-1

        Comparison.BruteSolution_cost=0
        Comparison.COUNT=0

        starttime_BG = datetime.datetime.now()
        task_ids=[i for i in range(0,task_num)]
        Comparison.BruteGreedy(task_ids, 0, task_num,users, tasks)
        totalcost_BG=Comparison.BruteSolution_cost
        endtime_BG = datetime.datetime.now()
        print('the final BruteSolution_cost is,', totalcost_BG)

        brute_greedy_usernum=0
        for user in users:
            if user.current_task_id==0:
                brute_greedy_usernum+=1

        Range_greedy_cost=Comparison.RangeGreedy(tasks,users)

        Random_cooperation_cost=Comparison.Random_cooperation(users,tasks)

        result_file.write('task num is %d\n'%task_num)

        result_file.write('CoalitionFormation\'s total participated user number is %d\n' % CF_participated_usernum)
        result_file.write('BruteGreedy\'s total participated user number is %d\n' % brute_greedy_usernum)

        result_file.write('Initial coalitionFormation\'s total cost is %d\n' % initial_totalcost_CF)
        result_file.write('Non_cooperation\'s total cost is %d\n' % totalcost_NC)
        result_file.write('CoalitionFormation\'s total cost is %d\n' % totalcost_CF)
        result_file.write('BruteGreedy\'s total cost is %d\n' % totalcost_BG)
        result_file.write('Random_cooperation\'s total cost is %d\n' % Random_cooperation_cost)
        #result_file.write('Non_Cooperation_greedy\'s total cost is %d\n'%totalcost_NCG)
        result_file.write('Range_greedy\'s total cost is %d\n' % Range_greedy_cost)

        result_file.write('\n')

        result_file.write('Non-cooperation %f%%\n' % (totalcost_NC/Random_cooperation_cost*100))
        result_file.write('BruteGreedy %f%%\n' % (totalcost_BG/Random_cooperation_cost*100))
        result_file.write('Random_cooperation %f%%\n' % (Random_cooperation_cost/ Random_cooperation_cost * 100))
        result_file.write('Range_greedy %f%%\n' % (Range_greedy_cost/ Random_cooperation_cost * 100))
        result_file.write('CoalitionFormation %f%%\n' % (totalcost_CF / Random_cooperation_cost * 100))

        result_file.write('\n')

        result_file.write ('Running time of CoalitionFormation is %d second(s)\n'%(endtime_CF - starttime_CF).seconds)
        result_file.write ('Running time of BruteGreedy is %d second(s)\n'%(endtime_BG - starttime_BG).seconds)
        result_file.write('Iteration number of CoalitionFormation is %d\n' % iteration_number)

        result_file.write('\n\n')

    result_file.close()