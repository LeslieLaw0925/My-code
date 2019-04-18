from User import User
from Content import Content
from Task import Task
import math
import CoalitionFormation
import Comparison
import datetime
import networkx as nx
import Lower_bound

users=[]
contents=[]
tasks=[]

user_num=100
task_nums=[10,15,20,25,30,35]
#task_nums=[20]

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

        initial_totalcost_CF = 0
        for task in tasks:
            task.initilize()
            initial_totalcost_CF +=task.Initialize_cooperation(users)

            '''
            initial_totalcost_CF += task_cost
            print('task %d\' initial cost is %d'%(task.task_id,task_cost))

            print('task %d\'s initial cost of flow dict is' % task.task_id)
            print(task.current_flowdict[0])

            print('task %d\'s mc_graph is' % task.task_id)
            print(task.current_mc_graph.edge)

            print('task %d\'s current avalible members are' % task.task_id)
            print(task.current_avalible_users)
            print('task %d\'s current caching members are' % task.task_id)
            print(task.current_caching_users)
            for user_id in task.current_avalible_users:
                print('the cost of user %d of task %d is: %d' % (user_id, task.task_id, users[user_id].current_cost))

            print('\n')
            '''

        starttime_CF = datetime.datetime.now()
        CF_result=CoalitionFormation.coalitionFormation(users,tasks)
        totalcost_CF=CF_result[0]
        CF_participated_usernum=CF_result[1]
        iteration_number=CF_result[2]

        endtime_CF = datetime.datetime.now()

        '''
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
        '''

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
        # Lowerbound
        LB_results = Lower_bound.LB_results(tasks, users)
        LB_cost = LB_results[0]
        LB_device_number = LB_results[1]

        print('initial_cost is', initial_totalcost_CF)
        print('CF_cost is',totalcost_CF)
        print('Lower bound is',LB_cost)

        for user in users:
            user.current_task_id=-1

        # overlap_brute_greedy和nonoverlap_brute_greedy算法
        Comparison.overlap_BruteSolution_cost = 0
        Comparison.overlap_brute_greedy_usernum = 0
        Comparison.COUNT = 0
        Comparison.non_overlap_BruteSolution_cost = 0
        Comparison.non_overlap_brute_greedy_usernum = 0

        starttime_BG = datetime.datetime.now()
        Comparison.BruteGreedy(users, tasks)
        endtime_BG = datetime.datetime.now()

        Range_greedy_cost=Comparison.RangeGreedy(tasks,users)

        #Random_cooperation_cost=Comparison.Random_cooperation(users,tasks)

        result_file.write('task num is %d\n'%task_num)

        result_file.write('CoalitionFormation\'s total participated user number is %d\n' % CF_participated_usernum)
        result_file.write('overlap_BruteGreedy\'s total participated user number is %d\n' % Comparison.overlap_brute_greedy_usernum)
        result_file.write('non_overlap_BruteGreedy\'s total participated user number is %d\n' % Comparison.non_overlap_brute_greedy_usernum)
        result_file.write('Lower bound\'s total participated user number is %d\n' % LB_device_number)

        result_file.write('Initial coalitionFormation\'s total cost is %d\n' % initial_totalcost_CF)
        result_file.write('Non_cooperation\'s total cost is %d\n' % totalcost_NC)
        result_file.write('CoalitionFormation\'s total cost is %d\n' % totalcost_CF)
        result_file.write('overlap_BruteGreedy\'s total cost is %d\n' % Comparison.overlap_BruteSolution_cost)
        result_file.write('non_overlap_BruteGreedy\'s total cost is %d\n' % Comparison.non_overlap_BruteSolution_cost)
        #result_file.write('Random_cooperation\'s total cost is %d\n' % Random_cooperation_cost)
        #result_file.write('Non_Cooperation_greedy\'s total cost is %d\n'%totalcost_NCG)
        result_file.write('Range_greedy\'s total cost is %d\n' % Range_greedy_cost)
        result_file.write('Lower bound is %d\n' % LB_cost)
        result_file.write('\n')

        result_file.write('Average device energy of CF is %f\n'% (totalcost_CF/CF_participated_usernum*math.pow(10,-10)))
        result_file.write('Average device energy of Non_cooperation is %f\n' % (totalcost_NC / task_num*math.pow(10,-10)))
        result_file.write('Average device energy of overlap_BruteGreedy is %f\n' % (Comparison.overlap_BruteSolution_cost / Comparison.overlap_brute_greedy_usernum*math.pow(10,-10)))
        result_file.write('Average device energy of non_overlap_BruteGreedy is %f\n' % (Comparison.non_overlap_BruteSolution_cost / Comparison.non_overlap_brute_greedy_usernum*math.pow(10,-10)))

        result_file.write('\n')
        '''
        result_file.write('Non-cooperation %f%%\n' % (totalcost_NC/Random_cooperation_cost*100))
        result_file.write('overlap_BruteGreedy %f%%\n' % (Comparison.overlap_BruteSolution_cost/Random_cooperation_cost*100))
        result_file.write('Random_cooperation %f%%\n' % (Random_cooperation_cost/ Random_cooperation_cost * 100))
        result_file.write('Range_greedy %f%%\n' % (Range_greedy_cost/ Random_cooperation_cost * 100))
        result_file.write('CoalitionFormation %f%%\n' % (totalcost_CF / Random_cooperation_cost * 100))

        result_file.write('\n')
        '''
        result_file.write ('Running time of CoalitionFormation is %d second(s)\n'%(endtime_CF - starttime_CF).seconds)
        result_file.write ('Running time of BruteGreedy is %d second(s)\n'%(endtime_BG - starttime_BG).seconds)
        result_file.write('Iteration number of CoalitionFormation is %d\n' % iteration_number)

        result_file.write('\n\n')

    result_file.close()