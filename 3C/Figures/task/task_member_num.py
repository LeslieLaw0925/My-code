import numpy as np
import matplotlib.pyplot as plt

#task_num = ['10','12','14','16','18','20']
task_num = ['10','15','20','25','30','35']

size = 6
x = np.arange(size)

CF=[18,26,32,43,50,54]
overlap_BruteGreedy=[6,6,7,9,10,15]
non_overlap_BruteGreedy=[20,29,38,49,59,66]
lower_bound=[4,6,6,8,9,10]

total_width, n = 0.8, 6
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, lower_bound, width=width, label='Lower Bound')
plt.bar(x+width, overlap_BruteGreedy, width=width, label='Overlapping Brute Greedy strategy',tick_label = task_num)
plt.bar(x+2*width, CF, width=width,  label='F3C algorithm')
plt.bar(x+3*width, non_overlap_BruteGreedy, width=width, label='Non_overlapping Brute Greedy strategy')


plt.ylabel("Participated device number T'",fontsize=12)
plt.xlabel("Task number",fontsize=12)
plt.ylim(0,70)
plt.legend()
plt.show()

