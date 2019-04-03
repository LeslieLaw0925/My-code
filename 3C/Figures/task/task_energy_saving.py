import numpy as np
import matplotlib.pyplot as plt

#task_num = ['10','12','14','16','18','20']
task_num = ['10','15','20','25','30','35']

size = 6
x = np.arange(size)

Non_cooperation_saving_ratio=[86.823175,112.881982,111,110.056259,67.614282,87.831829]
BruteGreedy_saving_ratio=[43.906504,60.979813,63.5,67.198349,43.525776,58.649768]
Random_cooperation_saving_ratio=[100,100,100,100,100,100]
CoalitionFormation_saving_ratio=[31.640086,44.668541,48,52.353801,33.885165,45.746869]


total_width, n = 0.8, 5
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, Random_cooperation_saving_ratio, width=width, label='Random cooperation strategy')
plt.bar(x+width, Non_cooperation_saving_ratio, width=width,  label='Non-cooperation strategy',tick_label = task_num)
plt.bar(x+2*width, BruteGreedy_saving_ratio, width=width, label='Brute Greedy strategy')
plt.bar(x+3*width, CoalitionFormation_saving_ratio, width=width, label='F3C algorithm')


plt.ylabel("Energy consumption ratio (%)",fontsize=12)
plt.xlabel("Task number",fontsize=12)
plt.ylim(0,170)
plt.legend()
plt.show()

