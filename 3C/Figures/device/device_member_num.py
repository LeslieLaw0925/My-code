import numpy as np
import matplotlib.pyplot as plt

device_num = ['70','80','90','100','120','150']

size = 6
x = np.arange(size)

CF=[48,50,50,51,53,55]
overlap_BruteGreedy=[15,14,17,15,15,15]
non_overlap_BruteGreedy=[60,59,56,59,57,55]
lower_bound=[10,11,10,10,12,12]

total_width, n = 0.8, 6
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, lower_bound, width=width, label='Lower Bound')
plt.bar(x+width, overlap_BruteGreedy, width=width, label='Overlapping Brute Greedy strategy',tick_label = device_num)
plt.bar(x+2*width, CF, width=width,  label='F3C algorithm')
plt.bar(x+3*width, non_overlap_BruteGreedy, width=width, label='Non_overlapping Brute Greedy strategy')


plt.ylabel("Participated device number T'",fontsize=12)
plt.xlabel("Fog device number",fontsize=12)
plt.ylim(0,81)
plt.legend()
plt.show()

