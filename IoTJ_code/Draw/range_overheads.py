import numpy as np
import matplotlib.pyplot as plt

user_ranges = ['50', '150', '350', '500']

size = 4
x = np.arange(size)

local_overheads=[40.127288,42.831537,43.675288,43.791868]
local_std=[1.64,1.9,2.0,2.14]

direct_cloud_overheads=[63.477829,65.127412,65.642098,65.713211]
cloud_std=[9.04,8.72,8.9,9.0]

greedy_overheads=[9.138496,13.225375,14.869816,14.955381]
greedy_std=[1.56,1.58,1.39,1.36]

random_overheads=[12.627731,17.526587,18.365374,18.320687]
random_std=[2.1,1.72,1.77,2.56]

total_width, n = 0.7, 4
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x , greedy_overheads, width=width, yerr=greedy_std,ecolor='#5b5b5b',capsize=2,label='Compared with greedy reciprocal pairing')
plt.bar(x+ width , random_overheads, width=width, yerr=random_std,ecolor='#5b5b5b',capsize=2,label='Compared with random reciprocal pairing')
plt.bar(x + 2*width,local_overheads, width=width, yerr=local_std,ecolor='#5b5b5b',capsize=2,label='Compared with local execution strategy',tick_label=user_ranges)
plt.bar(x + 3*width,direct_cloud_overheads, width=width, yerr=cloud_std,ecolor='#5b5b5b',capsize=2,label='Compared with fog execution strategy')

plt.ylabel("Performance gain in overhead (%)",fontsize=12)
plt.xlabel("D2D range",fontsize=12)
plt.ylim(0,110)
plt.legend()
plt.show()

