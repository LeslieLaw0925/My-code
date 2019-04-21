from User import User
from Content import Content
from Task import Task
import math
import CoalitionFormation
import Comparison
import datetime
import Formation_Comparison
import Lower_bound

users = []
contents = []
tasks = []

user_num = 150
task_nums = [10, 15, 20, 25, 30, 35]
user_range = 500

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

    result_file = open('Experiment/formation_task_num.docx', 'w')

    # 计算不同任务数目在系统中的表现

    for i in range(0, len(task_nums)):
        task_num = task_nums[i]

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
            user.current_task_id = -1
            for task in tasks:
                distance = math.sqrt(
                    math.pow((task.x_axis - task.x_axis), 2) + math.pow((task.y_axis - task.y_axis), 2))
                if distance < Task.task_range:
                    user.avalibleTasks.append(task.task_id)

        initial_totalcost_CF = 0
        for task in tasks:
            task.initilize()
            initial_totalcost_CF += task.Initialize_cooperation(users)

        starttime_CF = datetime.datetime.now()
        CF_result = CoalitionFormation.coalitionFormation(users, tasks)
        totalcost_CF = CF_result[0]
        CF_participated_usernum = CF_result[1]
        iteration_number = CF_result[2]
        endtime_CF = datetime.datetime.now()

        # Lowerbound
        LB_results = Lower_bound.LB_results(tasks, users)
        LB_cost = LB_results[0]
        LB_device_number = LB_results[1]

        print('initial_cost is', initial_totalcost_CF)
        print('CF_cost is', totalcost_CF)
        print('Lower bound is', LB_cost)

        Random_formation = Formation_Comparison.Random_formation(users, tasks)
        Greedy_formation = Formation_Comparison.Greedy_formation(users, tasks)

        '''
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

        Range_greedy_cost = Comparison.RangeGreedy(tasks, users)

        # Random_cooperation_cost=Comparison.Random_cooperation(users,tasks)
        '''

        result_file.write('task num is %d\n' % task_num)

        result_file.write('CoalitionFormation\'s total participated user number is %d\n' % CF_participated_usernum)
        result_file.write('Random Formation\'s total participated user number is %d\n' % Random_formation[1])
        result_file.write('Greedy Formation\'s total participated user number is %d\n' % Greedy_formation[1])
        result_file.write('Lower bound\'s total participated user number is %d\n' % LB_device_number)

        result_file.write('Initial coalitionFormation\'s total cost is %d\n' % initial_totalcost_CF)
        result_file.write('CoalitionFormation\'s total cost is %d\n' % totalcost_CF)
        result_file.write('Random Formation\'s total cost is %d\n' % Random_formation[0])
        result_file.write('Greedy Formation\'s total cost is %d\n' % Greedy_formation[0])
        result_file.write('Lower bound is %d\n' % LB_cost)
        result_file.write('\n')

        result_file.write('Running time of CoalitionFormation is %d second(s)\n' % (endtime_CF - starttime_CF).seconds)
        result_file.write('Iteration number of CoalitionFormation is %d\n' % iteration_number)

        result_file.write('\n\n')

    result_file.close()