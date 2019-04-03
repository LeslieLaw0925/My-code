import numpy as np
import matplotlib.pyplot as plt

MCC_overheads=[165.487714,313.060067,603.338484,1066.171479,1493.279860]
MCC_std=[25.12,28.4,35.42,48.27,41.31]

mwmatching_overheads=[158.763164,288.143216,515.923493,889.100683,1227.241989]
mwmatching_std=[24.7,20.32,29.33,44.2,46.68]

random_overheads=[180.249701,349.044903,685.402705,1261.370211,1764.417999]
random_std=[22.5,26.42,40.31,57.9,48.35]

greedy_overheads=[173.177052,341.216973,677.751425,1214.628424,1707.238338]
greedy_std=[25.0,28.33,34.27,51.8,42.6]

user_nums = ['50','100','200','350','500']

size = 5
x = np.arange(size)

total_width, n = 0.9,5
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x , mwmatching_overheads, width=width, yerr=mwmatching_std,ecolor='#5b5b5b',capsize=2,label='Graph matching')
plt.bar(x+ width , MCC_overheads, width=width,yerr=MCC_std,color='red',ecolor='#5b5b5b',capsize=2, label='MCC formation',tick_label=user_nums)
plt.bar(x + 2*width, random_overheads, width=width,yerr=random_std,ecolor='#5b5b5b',capsize=2, label='Random reciprocal pairing strategy')
plt.bar(x + 3*width, greedy_overheads, width=width, yerr=greedy_std,ecolor='#5b5b5b',capsize=2,label='Greedy reciprocal pairing strategy')

plt.ylabel("Total amount of overhead of all devices",fontsize=12)
plt.xlabel("Number of devices",fontsize=12)
plt.ylim(0,1850)
plt.legend()
plt.show()
