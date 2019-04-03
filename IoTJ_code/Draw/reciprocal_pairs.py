#coding:UTF-8
import numpy as np
import matplotlib.pyplot as plt

#plt.xlabel("Number of devices",fontsize=12)
#plt.ylabel("Incentive Compatible Cooperation Proportion (%)",fontsize=12)

plt.xlabel("设备数目",fontsize=12)
#plt.ylabel("激励相容协同比率 (%)",fontsize=12)

plt.ylim(0,50)

MCC=[9.0,16.0,24.25,31.23,36.12]
MCC_std=[6.14,4.3,4.8,4.2,2.6]

mwmatching=[4.4,9.2,11.7,12.69,13.36]
mwmatching_std=[3,4.54,3.13,2.83,2.14]

greedy=[8.6,15.2,23.8,30.37,34.84]
greedy_std=[6.14,4.3,5.3,4.0,2.3]

random=[4.8,10.8,15.0,21.09,26.16]
random_std=[2,4.3,2.0,3.68,2.0]

user_nums = [50,100,200,350,500]

MCC_ratio=[]
mwmatching_ratio=[]
random_ratio=[]
greedy_ratio=[]

for i in range(0,len(user_nums)):
    MCC_ratio.append(MCC[i])
    mwmatching_ratio.append(mwmatching[i])
    random_ratio.append(random[i])
    greedy_ratio.append(greedy[i])

size = 5
x = np.arange(size)

total_width, n = 0.7,4
width = total_width / n
x = x - (total_width - width) / size

'''
plt.bar(x , mwmatching_ratio, width=width, yerr=mwmatching_std,ecolor='#5b5b5b',capsize=2,label='Graph matching')
plt.bar(x + width, random_ratio, width=width, yerr=random_std,ecolor='#5b5b5b',capsize=2,label='Random reciprocal pairing strategy',tick_label=['50','100','200','350','500'])
plt.bar(x + 2*width, greedy_ratio, width=width, yerr=greedy_std,ecolor='#5b5b5b',capsize=2,label='Greedy reciprocal pairing strategy')
plt.bar(x + 3*width, MCC_ratio, width=width, color='red',yerr=MCC_std,ecolor='#5b5b5b',capsize=2,label='MCC formation')
'''
plt.bar(x , mwmatching_ratio, width=width, ecolor='#5b5b5b',capsize=2,label='Graph matching')
plt.bar(x + width, random_ratio, width=width, ecolor='#5b5b5b',capsize=2,label='Random reciprocal pairing strategy',tick_label=['50','100','200','350','500'])
plt.bar(x + 2*width, greedy_ratio, width=width, ecolor='#5b5b5b',capsize=2,label='Greedy reciprocal pairing strategy')
plt.bar(x + 3*width, MCC_ratio, width=width, color='red',ecolor='#5b5b5b',capsize=2,label='MCC formation')
plt.legend()
plt.show()
