import numpy as np
import matplotlib.pyplot as plt

#task_num = ['10','12','14','16','18','20']
task_num = ['10','15','20','25','30','35']

size = 6
x = np.arange(size)

CF=[15,20,28,35,39,45]
BruteGreedy_saving_ratio=[7,8,9,9,9,9]

total_width, n = 0.6, 2
width = total_width / n
x =list(range(len(CF)))

plt.bar(x, CF, width=width, label='F3C algorithm',tick_label = task_num)
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, BruteGreedy_saving_ratio, width=width, label='Brute Greedy strategy')


plt.ylabel("Number of participated devices T'",fontsize=12)
plt.xlabel("Task number",fontsize=12)
plt.ylim(0,50)
plt.legend()
plt.show()

