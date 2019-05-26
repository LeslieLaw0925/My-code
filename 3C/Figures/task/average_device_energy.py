import numpy as np
import matplotlib.pyplot as plt
import math

task_num = ['10','15','20','25','30','35']

size = 6
x = np.arange(size)

CoalitionFormation=[0.245024,0.235351,0.257981,0.256966,0.235510,0.242366]
Non_cooperation=[1.363241,1.245281,1.5,1.500509,1.362005,1.220312]
Edge_CoCaCo=[1.090734,1.6,2.9,2.0,2.5,1.5]
non_overlap_BruteGreedy=[0.244889,0.219284,0.236089,0.240092,0.228529,0.221460]


total_width, n = 0.8, 4
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, non_overlap_BruteGreedy, width=width, label='Non-overlapping Brute Greedy strategy')
plt.bar(x+width, CoalitionFormation, width=width,  label='F3C algorithm',hatch='////')
plt.bar(x+2*width, Non_cooperation, width=width, label='Non-cooperation strategy',tick_label = task_num,hatch='....')
plt.bar(x+3*width, Edge_CoCaCo, width=width, label='Edge-CoCaCo strategy')

plt.ylabel(r"Average device energy consumption ($\times 10^{10}$)",fontsize=15)
plt.xlabel("Task number",fontsize=15)
plt.ylim(0,4.1)
plt.legend()
plt.show()

