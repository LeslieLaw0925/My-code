# coding:utf-8
import CalculatePreferencelists
import DecentralizedAlgorithm
import CentralizedAlgorithm
from User import User
from Task import Task
import Comparison_range
import numpy as np

average_overheads = []
user_ranges = [0,50,150,350,500]

average_cen_optimalexecution_times = []
average_cen_optimalexecution_energys = []
average_cen_optimalexecution_overheads = []

average_decen_optimalexecution_times=[]
average_decen_optimalexecution_energys=[]
average_decen_optimalexecution_overheads=[]

average_localexecution_times = []
average_localexecution_energys = []
average_localexecution_overheads = []

average_directTocloud_times = []
average_directTocloud_energys = []
average_directTocloud_overheads = []

average_greedyreciprocal_times = []
average_greedyreciprocal_energys = []
average_greedyreciprocal_overheads = []

average_randomreciprocal_times = []
average_randomreciprocal_energys = []
average_randomreciprocal_overheads = []

total_cen_optimalexecution_times = [0 for i in range(0,len(user_ranges))]
total_cen_optimalexecution_energys = [0 for i in range(0,len(user_ranges))]
total_cen_optimalexecution_overheads = [0 for i in range(0,len(user_ranges))]

total_decen_optimalexecution_times = [0 for i in range(0,len(user_ranges))]
total_decen_optimalexecution_energys = [0 for i in range(0,len(user_ranges))]
total_decen_optimalexecution_overheads = [0 for i in range(0,len(user_ranges))]

total_localexecution_times = [0 for i in range(0,len(user_ranges))]
total_localexecution_energys = [0 for i in range(0,len(user_ranges))]
total_localexecution_overheads = [0 for i in range(0,len(user_ranges))]

total_directTocloud_times = [0 for i in range(0,len(user_ranges))]
total_directTocloud_energys = [0 for i in range(0,len(user_ranges))]
total_directTocloud_overheads = [0 for i in range(0,len(user_ranges))]

total_greedyreciprocal_times = [0 for i in range(0,len(user_ranges))]
total_greedyreciprocal_energys = [0 for i in range(0,len(user_ranges))]
total_greedyreciprocal_overheads = [0 for i in range(0,len(user_ranges))]

total_randomreciprocal_times = [0 for i in range(0,len(user_ranges))]
total_randomreciprocal_energys = [0 for i in range(0,len(user_ranges))]
total_randomreciprocal_overheads = [0 for i in range(0,len(user_ranges))]

user_num = 500

def execute(iteration_time):
    localexecution_overhead_gains = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_ranges))]
    directTocloud_overhead_gains = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_ranges))]
    greedyreciprocal_overhead_gains = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_ranges))]
    randomreciprocal_overhead_gains = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_ranges))]

    users = []
    # reciprocalGraph=ReciprocalGraph(user_num)
    result_file = open('Experiment/time_execution_range.docx', 'w')

    for iteration in range(0,iteration_time):
        users.clear()

        for user_id in range(0, user_num):
            user = User(user_id)
            user.initialize()
            task = Task()
            task.setTimeWeight(1)
            user.setCurrentTask(task)
            users.append(user)

        for i in range(0, len(user_ranges)):
            user_range = user_ranges[i]

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
            print('Result of centralized algorithm of user num is %d:' % user_num)
            cen_results = CentralizedAlgorithm.centralizedAlgorithm(users, user_num)
            cen_reciprocalCycles = cen_results[0]
            cen_duration_time=cen_results[2]
            print(cen_reciprocalCycles)

            #执行decentralized算法
            print('Result of decentralized algorithm：')
            decen_results=DecentralizedAlgorithm.decentralizedAlgorithm(users,user_num)
            decen_reciprocalCycles=decen_results[0]
            decen_duration_time=decen_results[1]
            print(decen_reciprocalCycles)

            local_results = Comparison_range.local_effect(users)

            directToCloud_results = Comparison_range.directToCloud_effect(users)
            greedyreciprocal_results = Comparison_range.greedy_reciprocal_effect(users)

            cen_reciprocal_results = Comparison_range.cen_reciprocal_effect(users, cen_reciprocalCycles,cen_duration_time/60)
            decen_reciprocal_results = Comparison_range.decen_reciprocal_effect(users, decen_reciprocalCycles,decen_duration_time/60)
            randomreciprocal_results = Comparison_range.randomReciprocity_effect(users)

            total_cen_optimalexecution_times[i] += cen_reciprocal_results[1] / user_num
            total_cen_optimalexecution_energys[i] += cen_reciprocal_results[2] / user_num
            total_cen_optimalexecution_overheads[i] += cen_reciprocal_results[0] / user_num

            total_decen_optimalexecution_times[i] += decen_reciprocal_results[1] / user_num
            total_decen_optimalexecution_energys[i] += decen_reciprocal_results[2] / user_num
            total_decen_optimalexecution_overheads[i] += decen_reciprocal_results[0] / user_num

            total_localexecution_times[i] += local_results[1] / user_num
            total_localexecution_energys[i] += local_results[2] / user_num
            total_localexecution_overheads[i] += local_results[0] / user_num
            localexecution_overhead_gains[i][iteration] = (local_results[0] - cen_reciprocal_results[0]) / \
                                                          local_results[0] * 100

            total_directTocloud_times[i] += directToCloud_results[1] / user_num
            total_directTocloud_energys[i] += directToCloud_results[2] / user_num
            total_directTocloud_overheads[i] += directToCloud_results[0] / user_num
            directTocloud_overhead_gains[i][iteration] = (directToCloud_results[0] - cen_reciprocal_results[0]) / \
                                                         directToCloud_results[0] * 100

            total_greedyreciprocal_times[i] += greedyreciprocal_results[1] / user_num
            total_greedyreciprocal_energys[i] += greedyreciprocal_results[2] / user_num
            total_greedyreciprocal_overheads[i] += greedyreciprocal_results[0] / user_num
            greedyreciprocal_overhead_gains[i][iteration] = (greedyreciprocal_results[0] - cen_reciprocal_results[0]) / \
                                                            greedyreciprocal_results[0] * 100

            total_randomreciprocal_times[i] += randomreciprocal_results[1] / user_num
            total_randomreciprocal_energys[i] += randomreciprocal_results[2] / user_num
            total_randomreciprocal_overheads[i] += randomreciprocal_results[0] / user_num
            randomreciprocal_overhead_gains[i][iteration] = (randomreciprocal_results[0] - cen_reciprocal_results[0]) / \
                                                            randomreciprocal_results[0] * 100

    for i in range(0,len(user_ranges)):

        average_cen_optimalexecution_times.append(total_cen_optimalexecution_times[i] / iteration_time)
        average_cen_optimalexecution_energys.append(total_cen_optimalexecution_energys[i] / iteration_time)
        average_cen_optimalexecution_overheads.append(total_cen_optimalexecution_overheads[i] / iteration_time)

        average_decen_optimalexecution_times.append(total_decen_optimalexecution_times[i] / iteration_time)
        average_decen_optimalexecution_energys.append(total_decen_optimalexecution_energys[i] / iteration_time)
        average_decen_optimalexecution_overheads.append(total_decen_optimalexecution_overheads[i] / iteration_time)

        average_localexecution_times.append(total_localexecution_times[i] / iteration_time)
        average_localexecution_energys.append(total_localexecution_energys[i] / iteration_time)
        average_localexecution_overheads.append(total_localexecution_overheads[i] / iteration_time)

        average_directTocloud_times.append(total_directTocloud_times[i] / iteration_time)
        average_directTocloud_energys.append(total_directTocloud_energys[i] / iteration_time)
        average_directTocloud_overheads.append(total_directTocloud_overheads[i] / iteration_time)

        average_greedyreciprocal_times.append(total_greedyreciprocal_times[i] / iteration_time)
        average_greedyreciprocal_energys.append(total_greedyreciprocal_energys[i] / iteration_time)
        average_greedyreciprocal_overheads.append(total_greedyreciprocal_overheads[i] / iteration_time)

        average_randomreciprocal_times.append(total_randomreciprocal_times[i] / iteration_time)
        average_randomreciprocal_energys.append(total_randomreciprocal_energys[i] / iteration_time)
        average_randomreciprocal_overheads.append(total_randomreciprocal_overheads[i] / iteration_time)

        result_file.write('当用户数为%d，可达距离为%d时，结果如下:\n' % (user_num, user_ranges[i]))

        result_file.write('每个用户采用centralized策略处理任务所花费的平均开销为:%f\n' % (average_cen_optimalexecution_overheads[i]))
        result_file.write('每个用户采用centralized策略处理任务所花费的平均时间为:%f\n' % (average_cen_optimalexecution_times[i]))
        result_file.write('每个用户采用centralized策略处理任务所花费的平均能量为:%f\n' % (average_cen_optimalexecution_energys[i]))

        result_file.write('每个用户采用decentralized策略处理任务所花费的平均开销为:%f\n' % (average_decen_optimalexecution_overheads[i]))
        result_file.write('每个用户采用decentralized策略处理任务所花费的平均时间为:%f\n' % (average_decen_optimalexecution_times[i]))
        result_file.write('每个用户采用decentralized策略处理任务所花费的平均能量为:%f\n' % (average_decen_optimalexecution_energys[i]))

        result_file.write('全部用户本地处理任务所花费的平均开销为:%f\n' % (average_localexecution_overheads[i]))
        result_file.write('全部用户本地处理任务所花费的平均时间为:%f\n' % (average_localexecution_times[i]))
        result_file.write('全部用户本地处理任务所花费的平均能量为:%f\n' % (average_localexecution_energys[i]))

        result_file.write('全部用户直接上传云处理任务所花费的平均开销为:%f\n' % (average_directTocloud_overheads[i]))
        result_file.write('全部用户直接上传云处理任务所花费的平均时间为:%f\n' % (average_directTocloud_times[i]))
        result_file.write('全部用户直接上传云处理任务所花费的平均能量为:%f\n' % (average_directTocloud_energys[i]))

        result_file.write('随机配对算法处理任务所花费的平均开销为:%f\n' % (average_randomreciprocal_overheads[i]))
        result_file.write('随机配对算法处理任务所花费的平均时间为:%f\n' % (average_randomreciprocal_times[i]))
        result_file.write('随机配对算法任务所花费的平均能量为:%f\n' % (average_randomreciprocal_energys[i]))

        result_file.write('贪心配对算法处理任务所花费的平均开销为:%f\n' % (average_greedyreciprocal_overheads[i]))
        result_file.write('贪心配对算法处理任务所花费的平均时间为:%f\n' % (average_greedyreciprocal_times[i]))
        result_file.write('贪心配对算法任务所花费的平均能量为:%f\n' % (average_greedyreciprocal_energys[i]))

        result_file.write('对比全部用户全部本地处理，本文centralized算法平均开销下降：%f%%\n' % (
            (average_localexecution_overheads[i] - average_cen_optimalexecution_overheads[i]) /
            average_localexecution_overheads[i] * 100))
        result_file.write('对比全部用户全部本地处理，本文centralized算法平均时延下降：%f%%\n' % (
            (average_localexecution_times[i] - average_cen_optimalexecution_times[i]) / average_localexecution_times[
                i] * 100))
        result_file.write('对比全部用户全部本地处理，本文centralized算法平均能量下降：%f%%\n' % (
            (average_localexecution_energys[i] - average_cen_optimalexecution_energys[i]) /
            average_localexecution_energys[
                i] * 100))
        result_file.write('对比全部用户全部本地处理的标准差为：%f%%\n' % np.std(localexecution_overhead_gains[i]))






        result_file.write('对比全部用户上传云处理，本文centralized算法平均开销下降：%f%%\n' % (
            (average_directTocloud_overheads[i] - average_cen_optimalexecution_overheads[i]) /
            average_directTocloud_overheads[
                i] * 100))
        result_file.write(
            '对比全部用户上传云处理，本文centralized算法平均时延下降：%f%%\n' % (
            (average_directTocloud_times[i] - average_cen_optimalexecution_times[i]) /
            average_directTocloud_times[i] * 100))
        result_file.write(
            '对比全部用户上传云处理，本文centralized算法平均能量下降：%f%%\n' % (
                (average_directTocloud_energys[i] - average_cen_optimalexecution_energys[i]) /
                average_directTocloud_energys[i] * 100))
        result_file.write('对比全部用户上传云处理的标准差为：%f%%\n' % np.std(directTocloud_overhead_gains[i]))






        result_file.write('对比随机配对处理，本文centralized算法平均开销下降：%f%%\n' % (
        (average_randomreciprocal_overheads[i] - average_cen_optimalexecution_overheads[i]) /
        average_randomreciprocal_overheads[i] * 100))
        result_file.write(
            '对比随机配对处理，本文centralized算法平均时延下降：%f%%\n' % (
            (average_randomreciprocal_times[i] - average_cen_optimalexecution_times[i]) /
            average_randomreciprocal_times[i] * 100))
        result_file.write('对比随机配对处理，本文centralized算法平均能量下降：%f%%\n' % (
            (average_randomreciprocal_energys[i] - average_cen_optimalexecution_energys[i]) /
            average_randomreciprocal_energys[i] * 100))
        result_file.write('对比随机配对处理的标准差为：%f%%\n' % np.std(randomreciprocal_overhead_gains[i]))





        result_file.write('对比贪心配对处理，本文centralized算法平均开销下降：%f%%\n' % (
        (average_greedyreciprocal_overheads[i] - average_cen_optimalexecution_overheads[i]) /
        average_greedyreciprocal_overheads[i] * 100))
        result_file.write('对比贪心配对处理，本文centralized算法平均时延下降：%f%%\n' % (
        (average_greedyreciprocal_times[i] - average_cen_optimalexecution_times[i]) /
        average_greedyreciprocal_times[i] * 100))
        result_file.write('对比贪心配对处理，本文centralized算法平均能量下降：%f%%\n' % (
        (average_greedyreciprocal_energys[i] - average_cen_optimalexecution_energys[i]) /
        average_greedyreciprocal_energys[i] * 100))
        result_file.write('对比贪心配对处理的标准差为：%f%%\n' % np.std(greedyreciprocal_overhead_gains[i]))



        result_file.write('\n')

    result_file.close()

    average_overheads.append(average_cen_optimalexecution_overheads)
    average_overheads.append(average_decen_optimalexecution_overheads)
    average_overheads.append(average_localexecution_overheads)
    average_overheads.append(average_directTocloud_overheads)
    average_overheads.append(average_randomreciprocal_overheads)
    average_overheads.append(average_greedyreciprocal_overheads)

    return average_overheads
