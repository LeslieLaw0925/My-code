import numpy as np
import matplotlib.pyplot as plt

#task_num = ['10','12','14','16','18','20']
task_num = ['10','15','20','25','30','35']

size = 6
x = np.arange(size)

CF=[20,28,39,48,53,62]
RandomFormation=[24,39,52,64,78,89]
GreedyFormation=[30,45,60,75,90,105]

total_width, n = 0.8, 3
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, CF, width=width, label='F3C algorithm')
plt.bar(x+width, RandomFormation, width=width,  label='Random formation strategy',tick_label = task_num,hatch='////')
plt.bar(x+2*width, GreedyFormation, width=width, label='Greedy formation strategy strategy')


plt.ylabel("Participated device number T'",fontsize=15)
plt.xlabel("Task number",fontsize=15)
plt.ylim(0,110)
plt.legend()
plt.show()

