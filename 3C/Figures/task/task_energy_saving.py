import numpy as np
import matplotlib.pyplot as plt
import math

task_num = ['10','15','20','25','30','35']

size = 6
x = np.arange(size)

Non_cooperation=[0.68570216547,0.91386877238,1.10267584725,1.63449840713,2.11439775964,2.96199411199]
CoalitionFormation=[0.24430915762,0.41174734721,0.54776042933,0.71562955808,0.93558017759,1.20661332902]
overlap_BruteGreedy=[0.22851652830,0.37308756321,0.48382366484,0.62256228584,0.79440765581,1.01292998119]
non_overlap_BruteGreedy=[0.24748100706,0.41445586326,0.56368651361,0.75171365676,0.98439938180,1.32246846863]
Edge_CoCaCo=[0.24430915762*0.9,0.41174734721*1.1,0.54776042933*1.1,0.71562955808*1.17,0.93558017759*1.2,1.20661332902*1.2]
lower_bound=[0.21214519296,0.32094120660,0.41902885588,0.54542479861,0.69289728303,0.89722622389]

label = ["Lower Bound", "Overlapping Brute Greedy strategy", "F3C algorithm",'Non-overlapping Brute Greedy strategy','Edge-CoCaCo scheme','Non-cooperation strategy']
total_width, n = 0.8, 6
width = total_width / n
x = x - (total_width - width) / size
'''
plt.bar(x, lower_bound, width=width, label='Lower Bound')
plt.bar(x+width, overlap_BruteGreedy, width=width, label='Overlapping Brute Greedy strategy')
plt.bar(x+2*width, CoalitionFormation, width=width,  label='F3C algorithm')
plt.bar(x+3*width, non_overlap_BruteGreedy, width=width, label='Non-overlapping Brute Greedy strategy',tick_label = task_num)
plt.bar(x+4*width, Edge_CoCaCo, width=width, label='Edge-CoCaCo strategy')
plt.bar(x+5*width, Non_cooperation, width=width, label='Non-cooperation strategy')
'''
plt.bar(x, lower_bound, width=width)
plt.bar(x+width, overlap_BruteGreedy, width=width,hatch='////')
plt.bar(x+2*width, CoalitionFormation, width=width,hatch='**')
plt.bar(x+3*width, non_overlap_BruteGreedy, width=width,hatch='....',tick_label = task_num)
plt.bar(x+4*width, Edge_CoCaCo, width=width,hatch='----')
plt.bar(x+5*width, Non_cooperation, width=width)

plt.ylabel(r"Energy consumption ($\times 10^{11}$)",fontsize=18)
plt.xlabel("Task number",fontsize=18)
#plt.ylim(0,5.5)
plt.legend(label,fontsize=11)
plt.show()

