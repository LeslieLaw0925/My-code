# coding:utf-8
import CalculatePreferencelists
import DecentralizedAlgorithm
import CentralizedAlgorithm
from User import User
import numpy as np

from Task import Task
import Comparison_usernum
import random as rand
average_overheads = []

def execute(iteration_time):

    user_nums = [50,100,200,350,500]
    #user_nums=[2]
    users = []
    user_range=500

    counted_usernum=user_nums[0]

    average_cen_optimalexecution_times = []
    average_cen_optimalexecution_energys = []
    average_cen_optimalexecution_overheads = []

    average_decen_optimalexecution_times = []
    average_decen_optimalexecution_energys = []
    average_decen_optimalexecution_overheads = []

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

    total_cen_optimalexecution_times = [0 for i in range(0,len(user_nums))]
    total_cen_optimalexecution_energys = [0 for i in range(0,len(user_nums))]
    total_cen_optimalexecution_overheads = [0 for i in range(0,len(user_nums))]

    total_decen_optimalexecution_times = [0 for i in range(0,len(user_nums))]
    total_decen_optimalexecution_energys = [0 for i in range(0,len(user_nums))]
    total_decen_optimalexecution_overheads = [0 for i in range(0,len(user_nums))]

    total_localexecution_times = [0 for i in range(0,len(user_nums))]
    total_localexecution_energys = [0 for i in range(0,len(user_nums))]
    total_localexecution_overheads = [0 for i in range(0,len(user_nums))]
    localexecution_overhead_gains = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_nums))]

    total_directTocloud_times = [0 for i in range(0,len(user_nums))]
    total_directTocloud_energys = [0 for i in range(0,len(user_nums))]
    total_directTocloud_overheads = [0 for i in range(0,len(user_nums))]
    directTocloud_overhead_gains = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_nums))]

    total_greedyreciprocal_times = [0 for i in range(0,len(user_nums))]
    total_greedyreciprocal_energys = [0 for i in range(0,len(user_nums))]
    total_greedyreciprocal_overheads = [0 for i in range(0,len(user_nums))]
    greedyreciprocal_overhead_gains = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_nums))]

    total_randomreciprocal_times = [0 for i in range(0,len(user_nums))]
    total_randomreciprocal_energys = [0 for i in range(0,len(user_nums))]
    total_randomreciprocal_overheads = [0 for i in range(0,len(user_nums))]
    randomreciprocal_overhead_gains = [[0 for i in range(0, iteration_time)] for i in range(0, len(user_nums))]

    total_cen_iteration_number = [0 for i in range(0, len(user_nums))]
    total_decen_iteration_number = [0 for i in range(0, len(user_nums))]

    total_cen_signal_overheads = [0 for i in range(0, len(user_nums))]
    total_decen_signal_overheads = [0 for i in range(0, len(user_nums))]

    total_cen_delay = [0 for i in range(0, len(user_nums))]
    total_decen_delay = [0 for i in range(0, len(user_nums))]

    result_file = open('Experiment/usernum.docx', 'w')
    result_file.write('以下是时间权重为(0,1)内任意值的结果:\n')

    for iteration in range(0,iteration_time):
        users.clear()

        for i in range(0, len(user_nums)):
            user_num = user_nums[i]

            if i == 0:
                for user_id in range(0, user_nums[i]):
                    user = User(user_id)
                    user.initialize()
                    task = Task()
                    task.setTimeWeight(rand.uniform(0,1))
                    user.setCurrentTask(task)
                    users.append(user)
            else:
                for user_id in range(user_nums[i - 1], user_nums[i]):
                    user = User(user_id)
                    user.initialize()
                    task = Task()
                    task.setTimeWeight(rand.uniform(0,1))
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
                user.setPreferrencelist(user_range,users)

            CalculatePreferencelists.findPreferenceList(users, user_num)

            # 执行centralized算法
            print('Result of centralized algorithm :')
            cen_results = CentralizedAlgorithm.centralizedAlgorithm(users, user_num)
            cen_reciprocalCycles=cen_results[0]
            cen_duration_time=cen_results[2]
            print(cen_reciprocalCycles)

            #执行decentralized算法
            print('Result of decentralized algorithm：')
            decen_results = DecentralizedAlgorithm.decentralizedAlgorithm(users, user_num)
            decen_reciprocalCycles = decen_results[0]
            decen_duration_time=decen_results[2]
            print(decen_reciprocalCycles)

            cen_reciprocal_results = Comparison_usernum.cen_reciprocal_effect(users, cen_reciprocalCycles, counted_usernum,cen_duration_time/60)
            decen_reciprocal_results = Comparison_usernum.decen_reciprocal_effect(users, decen_reciprocalCycles,counted_usernum,decen_duration_time/60)
            local_results = Comparison_usernum.local_effect(users,counted_usernum)
            directToCloud_results = Comparison_usernum.directToCloud_effect(users,counted_usernum)
            greedyreciprocal_results = Comparison_usernum.greedy_reciprocal_effect(users,counted_usernum)
            ramdon_reciprocal_results = Comparison_usernum.randomreciprocal_effect(users,counted_usernum)

            total_cen_delay[i]+= (cen_duration_time*1000)
            total_decen_delay[i]+=(decen_duration_time*1000)

            total_cen_iteration_number[i] += cen_results[1]
            total_decen_iteration_number[i] += decen_results[1]

            total_cen_signal_overheads[i] += cen_results[3]
            total_decen_signal_overheads[i] += decen_results[3]

            total_cen_optimalexecution_times[i] += cen_reciprocal_results[1] / counted_usernum
            total_cen_optimalexecution_energys[i] +=cen_reciprocal_results[2] / counted_usernum
            total_cen_optimalexecution_overheads[i] +=cen_reciprocal_results[0] / counted_usernum

            total_decen_optimalexecution_times[i] +=decen_reciprocal_results[1] / counted_usernum
            total_decen_optimalexecution_energys[i] +=decen_reciprocal_results[2] / counted_usernum
            total_decen_optimalexecution_overheads[i] +=decen_reciprocal_results[0] / counted_usernum

            total_localexecution_times[i] +=local_results[1]/ counted_usernum
            total_localexecution_energys[i] +=local_results[2]/ counted_usernum
            total_localexecution_overheads[i]+=local_results[0]/ counted_usernum
            localexecution_overhead_gains[i][iteration] = (local_results[0] - cen_reciprocal_results[0]) / \
                                                          local_results[0] * 100

            total_directTocloud_times[i]+=directToCloud_results[1]/ counted_usernum
            total_directTocloud_energys[i]+=directToCloud_results[2]/ counted_usernum
            total_directTocloud_overheads[i]+=directToCloud_results[0]/ counted_usernum
            directTocloud_overhead_gains[i][iteration] = (directToCloud_results[0] - cen_reciprocal_results[0]) / \
                                                         directToCloud_results[0] * 100

            total_greedyreciprocal_times[i]+=greedyreciprocal_results[1]/ counted_usernum
            total_greedyreciprocal_energys[i]+=greedyreciprocal_results[2]/ counted_usernum
            total_greedyreciprocal_overheads[i]+=greedyreciprocal_results[0]/ counted_usernum
            greedyreciprocal_overhead_gains[i][iteration] = (greedyreciprocal_results[0] - cen_reciprocal_results[0]) / \
                                                            greedyreciprocal_results[0] * 100

            total_randomreciprocal_times[i]+=ramdon_reciprocal_results[1]/ counted_usernum
            total_randomreciprocal_energys[i]+=ramdon_reciprocal_results[2]/ counted_usernum
            total_randomreciprocal_overheads[i]+=ramdon_reciprocal_results[0]/ counted_usernum
            randomreciprocal_overhead_gains[i][iteration] = (ramdon_reciprocal_results[0] - cen_reciprocal_results[0]) / \
                                                            ramdon_reciprocal_results[0] * 100


    for i in range(0,len(user_nums)):

        average_cen_optimalexecution_times.append(total_cen_optimalexecution_times[i] / iteration_time)
        average_cen_optimalexecution_energys.append(total_cen_optimalexecution_energys[i] / iteration_time)
        average_cen_optimalexecution_overheads.append(total_cen_optimalexecution_overheads[i] / iteration_time)

        average_decen_optimalexecution_times.append(total_decen_optimalexecution_times[i] / iteration_time)
        average_decen_optimalexecution_energys.append(total_decen_optimalexecution_energys[i] / iteration_time)
        average_decen_optimalexecution_overheads.append(total_decen_optimalexecution_overheads[i] / iteration_time)

        average_localexecution_times.append(total_localexecution_times[i]/ iteration_time)
        average_localexecution_energys.append(total_localexecution_energys[i]/ iteration_time)
        average_localexecution_overheads.append(total_localexecution_overheads[i]/ iteration_time)

        average_directTocloud_times.append(total_directTocloud_times[i]/ iteration_time)
        average_directTocloud_energys.append(total_directTocloud_energys[i]/ iteration_time)
        average_directTocloud_overheads.append(total_directTocloud_overheads[i]/ iteration_time)

        average_greedyreciprocal_times.append(total_greedyreciprocal_times[i]/ iteration_time)
        average_greedyreciprocal_energys.append(total_greedyreciprocal_energys[i]/ iteration_time)
        average_greedyreciprocal_overheads.append(total_greedyreciprocal_overheads[i]/ iteration_time)

        average_randomreciprocal_times.append(total_randomreciprocal_times[i]/ iteration_time)
        average_randomreciprocal_energys.append(total_randomreciprocal_energys[i]/ iteration_time)
        average_randomreciprocal_overheads.append(total_randomreciprocal_overheads[i]/ iteration_time)

        result_file.write('当用户数为%d时，结果如下:\n' % user_nums[i])

        result_file.write('centralized算法的signal overhead为:%f\n' % (total_cen_signal_overheads[i] / iteration_time))
        result_file.write('decentralized算法的signal overhead为:%f\n' % (total_decen_signal_overheads[i] / iteration_time))

        result_file.write('centralized算法的迭代次数为:%f\n' % (total_cen_iteration_number[i] / iteration_time))
        result_file.write('decentralized算法的迭代次数为:%f\n' % (total_decen_iteration_number[i] / iteration_time))

        result_file.write('centralized算法的迭代用时为:%fms\n' % (total_cen_delay[i] / iteration_time))
        result_file.write('decentralized算法的迭代用时为:%fms\n' % (total_decen_delay[i] / iteration_time))

        result_file.write(
            '每个用户采用centralized策略处理任务所花费的平均开销为:%f\n' % (average_cen_optimalexecution_overheads[i]))
        result_file.write(
            '每个用户采用centralized策略处理任务所花费的平均时间为:%f\n' % (average_cen_optimalexecution_times[i] ))
        result_file.write(
            '每个用户采用centralized策略处理任务所花费的平均能量为:%f\n' % (average_cen_optimalexecution_energys[i] ))

        result_file.write(
            '每个用户采用decentralized策略处理任务所花费的平均开销为:%f\n' % (average_decen_optimalexecution_overheads[i]))
        result_file.write(
            '每个用户采用decentralized策略处理任务所花费的平均时间为:%f\n' % (average_decen_optimalexecution_times[i]))
        result_file.write(
            '每个用户采用decentralized策略处理任务所花费的平均能量为:%f\n' % (average_decen_optimalexecution_energys[i]))

        result_file.write(
            '全部用户本地处理任务所花费的平均开销为:%f\n' % (average_localexecution_overheads[i] ))
        result_file.write(
            '全部用户本地处理任务所花费的平均时间为:%f\n' % (average_localexecution_times[i] ))
        result_file.write(
            '全部用户本地处理任务所花费的平均能量为:%f\n' % (average_localexecution_energys[i]))

        result_file.write(
            '全部用户直接上传云处理任务所花费的平均开销为:%f\n' % (average_directTocloud_overheads[i]))
        result_file.write(
            '全部用户直接上传云处理任务所花费的平均时间为:%f\n' % (average_directTocloud_times[i]))
        result_file.write(
            '全部用户直接上传云处理任务所花费的平均能量为:%f\n' % (average_directTocloud_energys[i]))

        result_file.write(
            '随机配对算法处理任务所花费的平均开销为:%f\n' % (average_randomreciprocal_overheads[i]))
        result_file.write(
            '随机配对算法处理任务所花费的平均时间为:%f\n' % (average_randomreciprocal_times[i]))
        result_file.write(
            '随机配对算法任务所花费的平均能量为:%f\n' % (average_randomreciprocal_energys[i]))

        result_file.write(
            '贪心配对算法处理任务所花费的平均开销为:%f\n' % (average_greedyreciprocal_overheads[i]))
        result_file.write(
            '贪心配对算法处理任务所花费的平均时间为:%f\n' % (average_greedyreciprocal_times[i]))
        result_file.write(
            '贪心配对算法任务所花费的平均能量为:%f\n' % (average_greedyreciprocal_energys[i]))

        result_file.write('对比全部用户全部本地处理，本文centralized算法平均开销下降：%f%%\n' % ((average_localexecution_overheads[i]-average_cen_optimalexecution_overheads[i])/average_localexecution_overheads[i]*100))
        result_file.write('对比全部用户全部本地处理，本文centralized算法平均时延下降：%f%%\n' % ((average_localexecution_times[i]-average_cen_optimalexecution_times[i])/average_localexecution_times[i]*100))
        result_file.write('对比全部用户全部本地处理，本文centralized算法平均能量下降：%f%%\n' % ((average_localexecution_energys[i]-average_cen_optimalexecution_energys[i])/average_localexecution_energys[i]*100))
        result_file.write('对比全部用户全部本地处理的标准差为：%f%%\n' % np.std(localexecution_overhead_gains[i]))




        result_file.write('对比全部用户上传云处理，本文centralized算法平均开销下降：%f%%\n' % ((average_directTocloud_overheads[i] - average_cen_optimalexecution_overheads[i]) / average_directTocloud_overheads[i]*100))
        result_file.write(
            '对比全部用户上传云处理，本文centralized算法平均时延下降：%f%%\n' % ((average_directTocloud_times[i] - average_cen_optimalexecution_times[i]) /
            average_directTocloud_times[i]*100))
        result_file.write(
            '对比全部用户上传云处理，本文centralized算法平均能量下降：%f%%\n' % ((average_directTocloud_energys[i] - average_cen_optimalexecution_energys[i]) /
            average_directTocloud_energys[i]*100))
        result_file.write('对比全部用户上传云处理的标准差为：%f%%\n' % np.std(directTocloud_overhead_gains[i]))




        result_file.write('对比随机配对处理，本文centralized算法平均开销下降：%f%%\n' % ((
            average_randomreciprocal_overheads[i] - average_cen_optimalexecution_overheads[i]) /
                          average_randomreciprocal_overheads[i]*100))
        result_file.write(
            '对比随机配对处理，本文centralized算法平均时延下降：%f%%\n' % ((average_randomreciprocal_times[i] - average_cen_optimalexecution_times[i]) /
            average_randomreciprocal_times[i]*100))
        result_file.write(
            '对比随机配对处理，本文centralized算法平均能量下降：%f%%\n' % ((average_randomreciprocal_energys[i] - average_cen_optimalexecution_energys[i]) /
            average_randomreciprocal_energys[i]*100))
        result_file.write('对比随机配对处理的标准差为：%f%%\n' % np.std(randomreciprocal_overhead_gains[i]))




        result_file.write('对比贪心配对处理，本文centralized算法平均开销下降：%f%%\n' % ((
            average_greedyreciprocal_overheads[i] - average_cen_optimalexecution_overheads[i]) /
                          average_greedyreciprocal_overheads[i]*100))
        result_file.write(
            '对比贪心配对处理，本文centralized算法平均时延下降：%f%%\n' % ((average_greedyreciprocal_times[i] - average_cen_optimalexecution_times[i]) /
            average_greedyreciprocal_times[i]*100))
        result_file.write(
            '对比贪心配对处理，本文centralized算法平均能量下降：%f%%\n' % ((average_greedyreciprocal_energys[i] - average_cen_optimalexecution_energys[i]) /
            average_greedyreciprocal_energys[i]*100))
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



