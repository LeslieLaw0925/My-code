import numpy as np
import matplotlib.pyplot as plt

user_nums = ['50','100','200','350','500']

size = 5
x = np.arange(size)

local_overheads=[37.545046,38.806448,39.056759,39.380327,39.420503]
local_std=[4.1,4.0,4.1,4.6,4.9]

direct_cloud_overheads=[54.278534,55.201970,55.385215,55.622090,55.651502]
cloud_std=[6.45,6.37,6.16,6.08,6.2]

greedy_overheads=[8.141737,9.101381,10.358743,13.895996,14.855468]
greedy_std=[3.38,5.75,3.67,4.22,4.23]

random_overheads=[12.285517,13.992584,17.675595,18.161041,18.790001]
random_std=[4.5,8.3,8.86,10.04,13.58]

total_width, n = 0.7, 4
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, greedy_overheads, width=width, yerr=greedy_std,ecolor='#5b5b5b',capsize=2,label='Compared with greedy reciprocal pairing')
plt.bar(x + width , random_overheads, width=width, yerr=random_std,ecolor='#5b5b5b',capsize=2,label='Compared with random reciprocal pairing')
plt.bar(x + 2*width,local_overheads, width=width, yerr=local_std,ecolor='#5b5b5b',capsize=2,label='Compared with local execution strategy',tick_label=user_nums)
plt.bar(x + 3*width,direct_cloud_overheads, width=width, yerr=cloud_std,ecolor='#5b5b5b',capsize=2,label='Compared with fog execution strategy')

plt.ylabel("Performance gain in delay (%)",fontsize=12)
plt.xlabel("Number of devices",fontsize=12)
plt.ylim(0,90)
plt.legend()
plt.show()

