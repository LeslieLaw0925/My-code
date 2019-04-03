import numpy as np
import matplotlib.pyplot as plt

MCC_modes=[81.9,244.7,45.7,127.7]
MCC_std=[9.62,10.44,8.21,6.15]

mwwatching_modes=[1.6,315.3,1.3,180.9]
mwwatching_std=[0.91,5.23,0.64,5.36]

greedy_modes=[88.6,241.1,40.8,129.5]
greedy_std=[9.26,10.24,8.96,6.83]

random_modes=[95.6,228.8,43.2,132.4]
random_std=[9.58,10.24,7.83,6.09]

modes = ['Mode 1','Mode 2','Mode 3','Mode 4']

size = 4
x = np.arange(size)

total_width, n = 0.9,4
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, mwwatching_modes, width=width,yerr=mwwatching_std,ecolor='#5b5b5b',capsize=2, label='Graph matching')
plt.bar(x+width, MCC_modes, width=width,yerr=MCC_std,color='red',ecolor='#5b5b5b',capsize=2, label='MCC formation')
plt.bar(x + 2*width, random_modes, width=width,yerr=random_std,ecolor='#5b5b5b',capsize=2, label='Random reciprocal pairing strategy',tick_label=modes)
plt.bar(x + 3*width, greedy_modes, width=width, yerr=greedy_std,ecolor='#5b5b5b',capsize=2,label='Greedy reciprocal pairing strategy')

plt.ylabel("Device number",fontsize=12)
plt.xlabel("Modes",fontsize=12)
plt.ylim(0,350)
plt.legend()
plt.show()
