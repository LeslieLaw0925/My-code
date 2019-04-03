import numpy as np
import matplotlib.pyplot as plt

#user_ranges = ['50', '150', '350', '500']
user_ranges = [50,150,350,500]

size = 4
x = np.arange(size)

local_overheads=[33.027879,34.466247,35.074118,35.087595]
local_std=[3.4,3.4,3.6,3.61]

direct_cloud_overheads=[59.917269,60.778131,61.141940,61.150007]
cloud_std=[8.0,8.0,8.2,8.4]

greedy_overheads=[6.412463,8.913223,8.973345,10.337873]
greedy_std=[1.0,1.0,1.7,1.8]

random_overheads=[10.321095,13.357001,14.061243,14.220352]
random_std=[2.4,2.1,2.0,3.0]

total_width, n = 0.7, 4
width = total_width / n
x = x - (total_width - width) / size
#x = x - total_width  / size

plt.bar(x, greedy_overheads, width=width, yerr=greedy_std,ecolor='#5b5b5b',capsize=2,label='Compared with greedy reciprocal pairing')
plt.bar(x + width, random_overheads, width=width, yerr=random_std,ecolor='#5b5b5b',capsize=2,label='Compared with random reciprocal pairing')
plt.bar(x + 2*width,local_overheads, width=width, yerr=local_std,ecolor='#5b5b5b',capsize=2,label='Compared with local execution strategy',tick_label=user_ranges)
plt.bar(x + 3*width,direct_cloud_overheads, width=width, yerr=cloud_std,ecolor='#5b5b5b',capsize=2,label='Compared with fog execution strategy')

plt.ylabel("Performance gain in delay (%)",fontsize=12)
plt.xlabel("D2D range",fontsize=12)
plt.ylim(0,100)
plt.legend()
plt.show()

