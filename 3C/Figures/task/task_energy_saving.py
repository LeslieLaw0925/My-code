import numpy as np
import matplotlib.pyplot as plt
import math

task_num = ['10','15','20','25','30','35']

size = 6
x = np.arange(size)

Non_cooperation=[68570216547,91386877238,110267584725,163449840713,211439775964,296199411199]
CoalitionFormation=[24430915762,41174734721,54776042933,71562955808,93558017759,120661332902]
overlap_BruteGreedy=[22851652830,37308756321,48382366484,62256228584,79440765581,101292998119]
non_overlap_BruteGreedy=[24748100706,41445586326,56368651361,75171365676,98439938180,132246846863]
Edge_CoCaCo=[24430915762*0.9,41174734721*1.1,54776042933*1.1,71562955808*1.17,93558017759*1.2,120661332902*1.2]
lower_bound=[21214519296,32094120660,41902885588,54542479861,69289728303,89722622389]


total_width, n = 0.8, 6
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, lower_bound, width=width, label='Lower Bound')
plt.bar(x+width, overlap_BruteGreedy, width=width, label='Overlapping Brute Greedy strategy')
plt.bar(x+2*width, CoalitionFormation, width=width,  label='F3C algorithm')
plt.bar(x+3*width, non_overlap_BruteGreedy, width=width, label='Non-overlapping Brute Greedy strategy',tick_label = task_num)
plt.bar(x+4*width, Edge_CoCaCo, width=width, label='Edge-CoCaCo strategy')
plt.bar(x+5*width, Non_cooperation, width=width, label='Non-cooperation strategy')

plt.ylabel(r"Energy consumption ($\times 10^{11}$)",fontsize=18)
plt.xlabel("Task number",fontsize=18)
#plt.ylim(0,5.5)
plt.legend()
plt.show()

