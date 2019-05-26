import numpy as np
import matplotlib.pyplot as plt

task_num = ['10','15','20','25','30','35']

size = 6
x = np.arange(size)

CoalitionFormation=[0.22220858529/20,0.36179437186/28,0.48873219208/39,0.62469060543/48,0.78093006912/53,0.99579239567/62]
RandomFormation=[1.64410909784/24,1.56718681498/39,4.72102580564/52,4.69229586257/64,5.25563447718/78,4.61413868963/89]
GreedyFormation=[0.82279049794/30,1.77712308360/45,2.85080762710/60,2.63171676747/75,3.59325181244/90,3.80554915880/105]

total_width, n = 0.8, 3
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, CoalitionFormation, width=width,  label='F3C algorithm')
plt.bar(x+width, GreedyFormation, width=width, label='Greedy formation strategy',tick_label = task_num,hatch='////')
plt.bar(x+2*width, RandomFormation, width=width, label='Random formation strategy')

plt.ylabel(r"Average device energy consumption ($\times 10^{12}$)",fontsize=15)
plt.xlabel("Task number",fontsize=15)
plt.ylim(0,0.12)
plt.legend()
plt.show()
