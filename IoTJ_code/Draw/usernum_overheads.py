import numpy as np
import matplotlib.pyplot as plt

user_nums = ['50','100','200','350','500']

size = 5
x = np.arange(size)

local_overheads=[38.087282,39.023861,40.159597,40.405879,40.145089]
local_std=[4.6,4.6,4.6,4.8,5.0]

direct_cloud_overheads=[57.327500,57.973025,58.755816,58.925562,58.745816]
cloud_std=[8.7,8.6,8.3,8.3,8.7]

greedy_overheads=[10.645998,14.254375,14.896412,15.187649,15.482639]
greedy_std=[3.7,7.5,6.6,5.8,6.5]
#greedy_std=[3.8,6,6.85,4.6,6]

random_overheads=[14.145846,17.033410,20.964697,21.546827,23.147447]
random_std=[6.5,11.7,8.6,6.7,13.7]


total_width, n = 0.7, 4
width = total_width / n
x = x - (total_width - width) / size

#plt.bar(x, greedy_overheads, width=width,yerr=greedy_std,ecolor='#5b5b5b',capsize=2,label='Compared with greedy reciprocal pairing')
plt.bar(x , greedy_overheads, width=width, yerr=greedy_std,ecolor='#5b5b5b',capsize=2,label='Compared with greedy reciprocal pairing')
plt.bar(x + width, random_overheads, width=width, yerr=random_std,ecolor='#5b5b5b',capsize=2,label='Compared with random reciprocal pairing')
plt.bar(x + 2*width,local_overheads, width=width,yerr=local_std,ecolor='#5b5b5b',capsize=2,label='Compared with local execution strategy',tick_label=user_nums)
plt.bar(x + 3*width,direct_cloud_overheads, width=width,yerr=cloud_std,ecolor='#5b5b5b',capsize=2,label='Compared with fog execution strategy')

plt.ylabel("Performance gain in overhead (%)",fontsize=12)
plt.xlabel("Number of devices",fontsize=12)
plt.ylim(0,95)
plt.legend()
plt.show()

