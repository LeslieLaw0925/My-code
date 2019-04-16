from User import User
from Content import Content
from Task import Task
import math
import CoalitionFormation
import Comparison
import datetime
import Lower_bound
import networkx as nx

users=[]
contents=[]
tasks=[]

def execute():
    user_nums=[70,80,90,100,120,150]
    #user_nums = [70]
    task_num=30

    user_range=500

    for i in range(0, Content.content_num):
        content = Content(i)
        contents.append(content)

    for i in range(0, task_num):
        task = Task(contents, i)
        tasks.append(task)

    result_file = open('Experiment/device_num.docx', 'w')

    #在不同数目设备下，固定的任务数目在系统中的表现

    for i in range(0,len(user_nums)):
        user_num=user_nums[i]

        if i == 0:
            for i in range(0, user_nums[i]):
                user = User(i)
                user.initialize()
                users.append(user)

                for task in tasks:
                    distance = math.sqrt(
                        math.pow((task.x_axis - task.x_axis), 2) + math.pow((task.y_axis - task.y_axis), 2))
                    if distance < Task.task_range:
                        user.avalibleTasks.append(task.task_id)

        else:
            for i in range(user_nums[i - 1], user_nums[i]):
                user = User(i)
                user.initialize()
                users.append(user)

                for task in tasks:
                    distance = math.sqrt(
                        math.pow((task.x_axis - task.x_axis), 2) + math.pow((task.y_axis - task.y_axis), 2))
                    if distance < Task.task_range:
                        user.avalibleTasks.append(task.task_id)

        for user in users:
            user.current_task_id=-1
            user.avalibleCooperators.clear()
            user.D2D_rate_of_Cooperators.clear()
            user.setAvalibleCooperators(user_range,users)


        initial_total_cost=0
        for task in tasks:
            task.avalible_users.clear()
            task.caching_users.clear()
            task.user_distances.clear()
            task.initilize()

            task.setAvalibaleUsers(users)
            task.setCachingUsers(users)

            task_cost=task.Initialize_cooperation(users)
            print('current device number is', user_num)
            print('initialized task is', task.task_id)

            initial_total_cost+=task_cost

        # Lowerbound
        LB_results = Lower_bound.LB_results(tasks, users)
        LB_cost = LB_results[0]
        LB_device_number = LB_results[1]

        #本文CF算法
        starttime_CF = datetime.datetime.now()
        CF_result = CoalitionFormation.coalitionFormation(users, tasks)
        totalcost_CF = CF_result[0]
        CF_participated_usernum = CF_result[1]
        iteration_number = CF_result[2]
        endtime_CF = datetime.datetime.now()

        print('initial_total_cost is', initial_total_cost)
        print('CF cost is', totalcost_CF)
        print('Lowerbound is', LB_cost)

        for user in users:
            user.current_task_id = -1

        # overlap_brute_greedy和nonoverlap_brute_greedy算法
        Comparison.overlap_BruteSolution_cost = 0
        Comparison.overlap_brute_greedy_usernum = 0
        Comparison.COUNT = 0
        Comparison.non_overlap_BruteSolution_cost = 0
        Comparison.non_overlap_brute_greedy_usernum = 0

        starttime_BG = datetime.datetime.now()
        Comparison.BruteGreedy(users, tasks)
        endtime_BG = datetime.datetime.now()

        totalcost_NC=Comparison.Non_Cooperation(users,tasks)
        print('Non_Cooperation algorithm finished!')

        # 暴力搜索方案弃用
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
        # range_greedy算法
        Range_greedy_cost=Comparison.RangeGreedy(tasks,users)
        print('RangeGreedy algorithm finished!')

        '''
        Random_cooperation_cost=Comparison.Random_cooperation(users,tasks)
        print('Random_cooperation algorithm finished!')
        '''

        result_file.write('user number is %d\n'% user_num)

        result_file.write('CoalitionFormation\'s total participated user number is %d\n' % CF_participated_usernum)
        result_file.write('overlap_BruteGreedy\'s total participated user number is %d\n' %Comparison.overlap_brute_greedy_usernum)
        result_file.write('non_overlap_BruteGreedy\'s total participated user number is %d\n' % Comparison.non_overlap_brute_greedy_usernum)
        result_file.write('Lower bound\'s total participated user number is %d\n' % LB_device_number)

        result_file.write('Non_cooperation\'s total cost is %d\n' % totalcost_NC)
        result_file.write('CoalitionFormation\'s total cost is %d\n' % totalcost_CF)
        result_file.write('overlap_BruteGreedy\'s total cost is %d\n' % Comparison.overlap_BruteSolution_cost)
        result_file.write('non_overlap_BruteGreedy\'s total cost is %d\n' % Comparison.non_overlap_BruteSolution_cost)
        #result_file.write('Random_cooperation\'s total cost is %d\n' % Random_cooperation_cost)
        # result_file.write('Non_Cooperation_greedy\'s total cost is %d\n'%totalcost_NCG)
        result_file.write('Range_greedy\'s total cost is %d\n' % Range_greedy_cost)
        result_file.write('Lower bound is %d\n' % LB_cost)

        result_file.write('\n')

        '''
        result_file.write('Non-cooperation %f%%\n' % (totalcost_NC / Random_cooperation_cost * 100))
        result_file.write('BruteGreedy %f%%\n' % (totalcost_BG / Random_cooperation_cost * 100))
        result_file.write('Random_cooperation %f%%\n' % (Random_cooperation_cost / Random_cooperation_cost * 100))
        result_file.write('Range_greedy %f%%\n' % (Range_greedy_cost / Random_cooperation_cost * 100))
        result_file.write('CoalitionFormation %f%%\n' % (totalcost_CF / Random_cooperation_cost * 100))
        '''
        result_file.write('\n')

        result_file.write ('Running time of CoalitionFormation is %d second(s)\n'%(endtime_CF - starttime_CF).seconds)
        result_file.write ('Running time of BruteGreedy is %d second(s)\n'%(endtime_BG - starttime_BG).seconds)
        result_file.write ('Iteration number of CoalitionFormation is %d\n' % iteration_number)

        result_file.write('\n\n')


    result_file.close()