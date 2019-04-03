import numpy as np
import matplotlib.pyplot as plt

user_ranges = ['50', '150', '350', '500']

size = 4
x = np.arange(size)

local_overheads=[76.120185,76.838138,77.243531,77.309288]
local_std=[1.5,1.42,1.36,1.37]

direct_cloud_overheads=[59.993706,61.196507,61.875669,61.985833]
cloud_std=[12.1,11.6,11.44,11.44]

greedy_overheads=[8.275378,11.755348,12.263015,13.754222]
greedy_std=[2.4,2.0,1.51,1.62]

random_overheads=[15.792038,19.360342,20.794012,20.892379]
random_std=[2.7,3.3,3.0,3.74]

total_width, n = 0.7, 4
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, greedy_overheads, width=width, yerr=greedy_std,ecolor='#5b5b5b',capsize=2,label='Compared with greedy reciprocal pairing')
plt.bar(x + width, random_overheads, width=width, yerr=random_std,ecolor='#5b5b5b',capsize=2,label='Compared with random reciprocal pairing')
plt.bar(x + 2*width,direct_cloud_overheads, width=width, yerr=cloud_std,ecolor='#5b5b5b',capsize=2,label='Compared with fog execution strategy',tick_label=user_ranges)
plt.bar(x + 3*width,local_overheads, width=width, yerr=local_std,ecolor='#5b5b5b',capsize=2,label='Compared with local execution strategy')

plt.ylabel("Performance gain in energy (%)",fontsize=12)
plt.xlabel("D2D range",fontsize=12)
plt.ylim(0,110)
plt.legend()
plt.show()

