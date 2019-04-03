# coding:utf-8
import CalculatePreferencelists
import DecentralizedAlgorithm
import CentralizedAlgorithm
from User import User
from ReciprocalGraph import ReciprocalGraph
from Task import Task
import Comparison_usernum
import Comparison
import random as rand


def execute(threadID):
    cen_reciprocalCycles = None
    decen_reciprocalCycles = None
    user_nums = [50, 100, 200, 350, 500]
    users = []
    iteration_num = 1

    average_optimalexecution_overheads = []
    average_localexecution_overheads = []
    average_directTocloud_overheads = []
    average_greedyreciprocal_overheads = []
    average_randomreciprocal_overheads = []

    average_algorithm_iterations = []
    average_iteration_times = []

    total_overheads = [[0 for i in range(len(user_nums))] in range(5)]
    print('total_overheads is',total_overheads)

    for j in range(0, iteration_num):
        users.clear()

        for i in range(0, len(user_nums)):
            user_num = user_nums[i]

            if i == 0:
                for user_id in range(0, user_nums[i]):
                    user = User(user_id)
                    user.initialize()
                    task = Task()

                    task.setTimeWeight(rand.uniform(0, 1.0))

                    user.setCurrentTask(task)
                    users.append(user)
            else:
                for user_id in range(user_nums[i - 1], user_nums[i]):
                    user = User(user_id)
                    user.initialize()
                    task = Task()

                    task.setTimeWeight(rand.uniform(0, 1.0))

                    user.setCurrentTask(task)
                    users.append(user)

            for user in users:
                user.setPreferrencelist(user_num)

            total_algorithm_iteration = 0
            total_iteration_time = 0



            print('current iteration_num is', iteration_num)

            CalculatePreferencelists.findPreferenceList(users, user_num)

            # 执行centralized算法
            print('Result of centralized algorithm of user num is %d:' % user_num)
            results = CentralizedAlgorithm.centralizedAlgorithm(users, user_num)
            cen_reciprocalCycles = results[0]
            total_algorithm_iteration += results[1]
            total_iteration_time += results[2]
            print(cen_reciprocalCycles)

            '''#执行decentralized算法
            print('Result of decentralized algorithm：')
            decen_reciprocalCycles=DecentralizedAlgorithm.decentralizedAlgorithm(users,user_num)
            print(decen_reciprocalCycles)'''

            local_results = Comparison_usernum.local_effect(users)
            directToCloud_results = Comparison_usernum.directToCloud_effect(users)
            greedyreciprocal_results = Comparison_usernum.greedy_reciprocal_effect(users)
            reciprocal_results = Comparison_usernum.reciprocal_effect(users, cen_reciprocalCycles)
            ramdon_reciprocal_results = Comparison_usernum.randomreciprocal_effect(users)

            total_optimalexecution_overhead += reciprocal_results

            total_localexecution_overhead += local_results

            total_directTocloud_overhead += directToCloud_results

            total_greedyreciprocal_overhead += greedyreciprocal_results

            total_randomreciprocal_overhead += ramdon_reciprocal_results

    average_optimalexecution_overheads.append(total_optimalexecution_overhead / user_num / iteration_num)
    average_localexecution_overheads.append(total_localexecution_overhead / user_num / iteration_num)
    average_directTocloud_overheads.append(total_directTocloud_overhead / user_num / iteration_num)
    average_greedyreciprocal_overheads.append(total_greedyreciprocal_overhead / user_num / iteration_num)
    average_randomreciprocal_overheads.append(total_randomreciprocal_overhead / user_num / iteration_num)

    average_algorithm_iterations.append(total_algorithm_iteration / iteration_num)
    average_iteration_times.append(total_iteration_time / iteration_num)

    result_file = open('results_overhead.docx', 'w')
    result_file.write('以下是时间权重为(0,1)内任意值的结果:\n')

    for i in range(0, len(user_nums)):
        result_file.write('当用户数为%d时，结果如下:\n' % user_nums[i])

        result_file.write('平均迭代次数为:%d\n' % average_algorithm_iterations[i])
        result_file.write('平均迭代时间为:%f分钟\n' % average_iteration_times[i])

        result_file.write('每个任务采用本文策略处理任务所花费的平均开销为:%f\n' % average_optimalexecution_overheads[i])

        result_file.write('全部任务本地处理任务所花费的平均开销为:%f\n' % average_localexecution_overheads[i])

        result_file.write('全部任务直接上传云处理任务所花费的平均开销为:%f\n' % average_directTocloud_overheads[i])

        result_file.write('贪心匹配算法处理任务所花费的平均开销为:%f\n' % average_greedyreciprocal_overheads[i])

        result_file.write('随机匹配处理任务所花费的平均开销为:%f\n' % average_randomreciprocal_overheads[i])

        result_file.write("对比全部用户本地处理任务，本文策略平均开销下降了%f%%\n" % (
            (average_localexecution_overheads[i] - average_optimalexecution_overheads[i]) /
            average_localexecution_overheads[i] * 100))

        result_file.write('对比全部用户直接上传云处理任务，本文策略平均开销下降了%f%%\n' % (
            (average_directTocloud_overheads[i] - average_optimalexecution_overheads[i]) /
            average_directTocloud_overheads[i] * 100))

        result_file.write('对比贪心匹配算法处理任务，本文策略平均开销下降了%f%%\n' % (
            (average_greedyreciprocal_overheads[i] - average_optimalexecution_overheads[i]) /
            average_greedyreciprocal_overheads[i] * 100))

        result_file.write('对比随机匹配策略处理任务，本文策略平均开销下降了%f%%\n' % (
            (average_randomreciprocal_overheads[i] - average_optimalexecution_overheads[i]) /
            average_randomreciprocal_overheads[i] * 100))

        result_file.write('\n')

    result_file.close()