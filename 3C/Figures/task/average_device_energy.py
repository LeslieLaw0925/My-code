import numpy as np
import matplotlib.pyplot as plt
import math

task_num = ['10','15','20','25','30','35']

size = 6
x = np.arange(size)

CoalitionFormation=[0.245024,0.235351,0.257981,0.256966,0.235510,0.242366]
Non_cooperation=[1.363241,1.245281,1.5,1.500509,1.362005,1.220312]
#overlap_BruteGreedy=[0.822244,0.845838,0.852749,0.913315,0.703184,0.768791]
non_overlap_BruteGreedy=[0.244889,0.219284,0.236089,0.240092,0.228529,0.221460]
#range_greedy=[60495737257,84065496092,107752125150,163008996835,241209918044,304356212699]
#lower_bound=[21214519296,32094120660,41902885588,54542479861,69289728303,89722622389]


total_width, n = 0.8, 4
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, non_overlap_BruteGreedy, width=width, label='Non-overlapping Brute Greedy strategy')
plt.bar(x+width, CoalitionFormation, width=width,  label='F3C algorithm',tick_label = task_num)
#plt.bar(x+2*width, overlap_BruteGreedy, width=width, label='Overlapping Brute Greedy strategy')
plt.bar(x+2*width, Non_cooperation, width=width, label='Non-cooperation strategy')

plt.ylabel(r"Average device energy consumption ($\times 10^{10}$)",fontsize=12)
plt.xlabel("Task number",fontsize=12)
plt.ylim(0,2.1)
plt.legend()
plt.show()

