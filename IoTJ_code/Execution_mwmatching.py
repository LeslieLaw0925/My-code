# coding:utf-8
import CalculatePreferencelists
import CentralizedAlgorithm
from User import User

from Task import Task
import Comparison_mwmatching
import random as rand
import numpy as np

average_overheads = []


def execute(iteration_time):
    user_nums = [50,100,200,350,500]
    users = []
    user_range =500

    average_cen_optimalexecution_overheads = []
    average_mwmatching_overheads=[]
    average_greedy_reciprocal_overheads=[]
    average_random_reciprocal_overheads=[]

    total_cen_optimalexecution_overheads = [0 for i in range(0, len(user_nums))]
    total_mwmatching_overheads = [0 for i in range(0, len(user_nums))]
    total_greedy_reciprocal_overheads = [0 for i in range(0, len(user_nums))]
    total_random_reciprocal_overheads = [0 for i in range(0, len(user_nums))]

    cen_reciprocal_beneficial_usernum=[0 for i in range(0, len(user_nums))]
    mwmatching_reciprocal_beneficial_usernum=[0 for i in range(0, len(user_nums))]
    greedy_reciprocal_beneficial_usernum=[0 for i in range(0, len(user_nums))]
    random_reciprocal_beneficial_usernum=[0 for i in range(0, len(user_nums))]

    cen_reciprocal_overheads=[[0 for i in range(0, iteration_time)] for i in range(0, len(user_nums))]
    mwmatching_reciprocal_overheads=[[0 for i in range(0, iteration_time)] for i in range(0, len(user_nums))]
    greedyreciprocal_overheads = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_nums))]
    randomreciprocal_overheads = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_nums))]

    cen_reciprocal_beneficial_usernums = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_nums))]
    mwmatching_reciprocal_beneficial_usernums = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_nums))]
    greedyreciprocal_beneficial_usernums = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_nums))]
    randomreciprocal_beneficial_usernums = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_nums))]

    cen_optimalexecution_modes = [[0 for i in range(0, iteration_time)] for i in range(0, 4)]
    mwmatching_modes = [[0 for i in range(0, iteration_time)] for i in range(0, 4)]
    greedy_reciprocal_modes = [[0 for i in range(0, iteration_time)] for i in range(0, 4)]
    random_reciprocal_modes = [[0 for i in range(0, iteration_time)] for i in range(0, 4)]

    result_file = open('Experiment/mwmatching.docx', 'w')
    result_file.write('以下是时间权重为(0,1)内任意值的结果:\n')

    for iteration in range(0, iteration_time):
        users.clear()

        for i in range(0, len(user_nums)):
            '''
            cen_optimalexecution_modes.clear()
            mwmatching_modes.clear()
            greedy_reciprocal_modes.clear()
            random_reciprocal_modes.clear()
            '''

            user_num = user_nums[i]

            if i == 0:
                for user_id in range(0, user_nums[i]):
                    user = User(user_id)
                    user.initialize()
                    task = Task()
                    task.setTimeWeight(rand.uniform(0, 1))
                    user.setCurrentTask(task)
                    users.append(user)
            else:
                for user_id in range(user_nums[i - 1], user_nums[i]):
                    user = User(user_id)
                    user.initialize()
                    task = Task()
                    task.setTimeWeight(rand.uniform(0, 1))
                    user.setCurrentTask(task)
                    users.append(user)

            for user in users:
                user.strategylist.clear()  # 策略列表
                user.overheads.clear()  # helpers的消耗列表
                user.time_overheads.clear()  # helpers的时间消耗列表
                user.energy_overheads.clear()  # helpers的能量消耗列表
                user.preference_list.clear()  # user的helper排序列表
                user.most_preferred_helper_id = None
                user.flag = 0
                user.setPreferrencelist(user_range, users)

            CalculatePreferencelists.findPreferenceList(users, user_num)

            # 执行centralized算法
            print('Result of centralized algorithm :')
            cen_results = CentralizedAlgorithm.centralizedAlgorithm(users, user_num)
            cen_reciprocalCycles = cen_results[0]
            print(cen_reciprocalCycles)

            cen_reciprocal_results = Comparison_mwmatching.cen_reciprocal_effect(users,cen_reciprocalCycles)
            mwmathcing_results=Comparison_mwmatching.execute_mwmatching(users)
            greedy_reciprocal_results=Comparison_mwmatching.greedy_reciprocal_effect(users)
            random_reciprocal_results=Comparison_mwmatching.randomreciprocal_effect(users)

            total_cen_optimalexecution_overheads[i] += cen_reciprocal_results[0]
            total_mwmatching_overheads[i] += mwmathcing_results[0]
            total_greedy_reciprocal_overheads[i]+=greedy_reciprocal_results[0]
            total_random_reciprocal_overheads[i]+=random_reciprocal_results[0]

            cen_reciprocal_beneficial_usernum[i] += cen_reciprocal_results[1]
            mwmatching_reciprocal_beneficial_usernum[i] += mwmathcing_results[1]
            greedy_reciprocal_beneficial_usernum[i]+=greedy_reciprocal_results[1]
            random_reciprocal_beneficial_usernum[i]+=random_reciprocal_results[1]

            cen_reciprocal_overheads[i][iteration] =  cen_reciprocal_results[0]
            mwmatching_reciprocal_overheads [i][iteration] =  mwmathcing_results[0]
            greedyreciprocal_overheads[i][iteration] =  greedy_reciprocal_results[0]
            randomreciprocal_overheads [i][iteration] =  random_reciprocal_results[0]

            cen_reciprocal_beneficial_usernums[i][iteration] = cen_reciprocal_results[1]/user_nums[i]*100
            mwmatching_reciprocal_beneficial_usernums [i][iteration] =  mwmathcing_results[1]/user_nums[i]*100
            greedyreciprocal_beneficial_usernums[i][iteration] =  greedy_reciprocal_results[1]/user_nums[i]*100
            randomreciprocal_beneficial_usernums [i][iteration] =  random_reciprocal_results[1]/user_nums[i]*100

            for j in range(0,4):
                cen_optimalexecution_modes[j][iteration]=cen_reciprocal_results[2][j]
                mwmatching_modes[j][iteration]=mwmathcing_results[2][j]
                greedy_reciprocal_modes[j][iteration]=greedy_reciprocal_results[2][j]
                random_reciprocal_modes[j][iteration]=random_reciprocal_results[2][j]


    for i in range(0, len(user_nums)):
        average_cen_optimalexecution_overheads.append(total_cen_optimalexecution_overheads[i] / iteration_time)
        average_mwmatching_overheads.append(total_mwmatching_overheads[i]/iteration_time)
        average_greedy_reciprocal_overheads.append(total_greedy_reciprocal_overheads[i]/iteration_time)
        average_random_reciprocal_overheads .append(total_random_reciprocal_overheads[i]/iteration_time)

        result_file.write('当用户数为%d时，结果如下:\n' % user_nums[i])

        result_file.write(
            '采用centralized策略处理任务所花费的系统总开销为:%f\n' % (average_cen_optimalexecution_overheads[i]))
        result_file.write(
            '采用mwmatching策略处理任务所花费的系统总开销为:%f\n' % (average_mwmatching_overheads[i]))
        result_file.write(
            '采用greedy策略处理任务所花费的系统总开销为:%f\n' % (average_greedy_reciprocal_overheads[i]))
        result_file.write(
            '采用random策略处理任务所花费的系统总开销为:%f\n' % (average_random_reciprocal_overheads[i]))


        result_file.write(
            '采用centralized策略处理任务的benefical user的ICCR是:%f%%\n' % (cen_reciprocal_beneficial_usernum[i]/iteration_time/user_nums[i]*100))
        result_file.write(
            '采用mwmatching策略处理任务所花费的benefical user的ICCR是:%f%%\n' % (mwmatching_reciprocal_beneficial_usernum[i]/iteration_time/user_nums[i]*100))
        result_file.write(
            '采用greedy策略处理任务所花费的benefical user的ICCR是:%f%%\n' % (
                greedy_reciprocal_beneficial_usernum[i] / iteration_time/user_nums[i]*100))
        result_file.write(
            '采用random策略处理任务所花费的benefical user的ICCR是:%f%%\n' % (
                random_reciprocal_beneficial_usernum[i] / iteration_time/user_nums[i]*100))

        result_file.write('对比mwmatching策略，本文centralized算法平均系统总开销提高：%f%%\n' % (
            (average_cen_optimalexecution_overheads[i] - average_mwmatching_overheads[i]) /
            average_cen_optimalexecution_overheads[i]*100))



        result_file.write(
            '采用centralized策略处理任务所花费的标准差为:%f\n' % (np.std(cen_reciprocal_overheads[i])))
        result_file.write(
            '采用mwmatching策略处理任务所花费的标准差为:%f\n' % (np.std(mwmatching_reciprocal_overheads[i])))
        result_file.write(
            '采用greedy策略处理任务所花费的标准差为:%f\n' % (np.std(greedyreciprocal_overheads[i])))
        result_file.write(
            '采用random策略处理任务所花费的标准差为:%f\n' % (np.std(randomreciprocal_overheads[i])))

        result_file.write(
            '采用centralized策略ICCR的标准差为:%f\n' % (np.std(cen_reciprocal_beneficial_usernums[i])))
        result_file.write(
            '采用mwmatching策略ICCR的标准差为:%f\n' % (np.std(mwmatching_reciprocal_beneficial_usernums[i])))
        result_file.write(
            '采用greedy策略ICCR的标准差为:%f\n' % (np.std(greedyreciprocal_beneficial_usernums[i])))
        result_file.write(
            '采用random策略ICCR的标准差为:%f\n' % (np.std(randomreciprocal_beneficial_usernums[i])))

        for j in range(0, 4):
            result_file.write('\n')
            result_file.write(
                '采用centralized策略mode%d的数目%f\n'%(j+1,sum(cen_optimalexecution_modes[j])/iteration_time))
            result_file.write(
                '采用centralized策略mode%d的标准差为:%f\n' % (j+1,np.std(cen_optimalexecution_modes[j])))

            result_file.write(
                '采用mwmatching策略mode%d的数目%f\n'%(j+1, sum(mwmatching_modes[j])/iteration_time))
            result_file.write(
                '采用mwmatching策略mode%d的标准差为:%f\n' % (j+1,np.std(mwmatching_modes[j])))

            result_file.write(
                '采用greedy策略mode%d的数目%f\n'%(j+1,sum(greedy_reciprocal_modes[j])/iteration_time))
            result_file.write(
                '采用greedy策略mode%d的标准差为:%f\n'% (j+1,np.std(greedy_reciprocal_modes[j])))

            result_file.write(
                '采用random策略mode%d的数目%f\n'%(j+1,sum(random_reciprocal_modes[j])/iteration_time))
            result_file.write(
                '采用random策略mode%d的标准差为:%f\n' % (j+1,np.std(random_reciprocal_modes[j])))


        result_file.write('\n')

    result_file.close()



