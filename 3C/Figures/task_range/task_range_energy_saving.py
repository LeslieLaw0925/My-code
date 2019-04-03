import numpy as np
import matplotlib.pyplot as plt

#task_num = ['10','12','14','16','18','20']
task_num = ['100','200','300','400','500','600']

size = 6
x = np.arange(size)

Non_cooperation_saving_ratio=[54.993792,52.283241,43.651663,56.839149,74.403412,30.923624]
BruteGreedy_saving_ratio=[42.054123,38.593912,30.324027,40.365390,52.908739,21.853898]
Random_cooperation_saving_ratio=[100,100,100,100,100,100]
CoalitionFormation_saving_ratio=[34.321358,32.399819,26.782166,35.071662,45.288843,18.751005]

total_width, n = 0.8, 5
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, Random_cooperation_saving_ratio, width=width, label='Random cooperation strategy')
plt.bar(x+width, Non_cooperation_saving_ratio, width=width,  label='Non-cooperation strategy')
plt.bar(x+2*width, BruteGreedy_saving_ratio, width=width, label='Brute Greedy strategy',tick_label = task_num)
plt.bar(x+3*width, CoalitionFormation_saving_ratio, width=width, label='Task Team Formation strategy')


plt.ylabel("Performance gain in energy (%)",fontsize=12)
plt.xlabel("Task range",fontsize=12)
plt.ylim(0,170)
plt.legend()
plt.show()

