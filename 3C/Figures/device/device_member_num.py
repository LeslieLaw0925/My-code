import numpy as np
import matplotlib.pyplot as plt

device_num = ['70','80','90','100','120','150']

size = 6
x = np.arange(size)

CF=[48,50,50,51,53,55]
Edge_CoCaCo=[12,11,12,12,13,11]
non_overlap_BruteGreedy=[60,59,56,59,57,55]
#lower_bound=[10,11,10,10,12,12]
non_cooperation=[30,30,30,30,30,30]

total_width, n = 0.8, 4
width = total_width / n
x = x - (total_width - width) / size


plt.bar(x, Edge_CoCaCo, width=width, label='Edge-CoCaCo strategy')
plt.bar(x+width, non_cooperation, width=width, label='Non-cooperation strategy')
plt.bar(x+2*width, CF, width=width,  label='F3C algorithm',tick_label = device_num)
plt.bar(x+3*width, non_overlap_BruteGreedy, width=width, label='Non-overlapping Brute Greedy strategy')


plt.ylabel("Participated device number T'",fontsize=15)
plt.xlabel("Fog device number",fontsize=15)
plt.ylim(0,81)
plt.legend()
plt.show()

