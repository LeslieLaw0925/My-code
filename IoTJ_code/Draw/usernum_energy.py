import numpy as np
import matplotlib.pyplot as plt

user_nums = ['50','100','200','350','500']

size = 5
x = np.arange(size)

local_overheads=[77.679826,77.969371,78.257422,78.264981,78.294306]
local_std=[3.47,3.56,3.48,3.47,3.5]

direct_cloud_overheads=[61.486485,61.986095,62.483129,62.496171,62.546771]
cloud_std=[19.8,19.7,19.7,19.83,19.5]

greedy_overheads=[4.750180,7.461095,9.953349,9.321981,11.165810]
greedy_std=[3.8,6,6.85,4.6,6]

random_overheads=[19.142995,18.690689,24.629226,24.935963,25.898473]
random_std=[7.4,18.2,11.12,17.17,18]

total_width, n = 0.7, 4
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x , greedy_overheads, width=width, yerr=greedy_std,ecolor='#5b5b5b',capsize=2,label='Compared with greedy reciprocal pairing')
plt.bar(x + width, random_overheads, width=width, yerr=random_std,ecolor='#5b5b5b',capsize=2,label='Compared with random reciprocal pairing')
plt.bar(x + 2*width,direct_cloud_overheads, width=width, yerr=cloud_std,ecolor='#5b5b5b',capsize=2,label='Compared with fog execution strategy',tick_label=user_nums)
plt.bar(x + 3*width,local_overheads, width=width,yerr=local_std,ecolor='#5b5b5b',capsize=2, label='Compared with local execution strategy')

plt.ylabel("Performance gain in energy(%)",fontsize=12)
plt.xlabel("Number of devices",fontsize=12)
plt.ylim(0,120)
plt.legend()
plt.show()

