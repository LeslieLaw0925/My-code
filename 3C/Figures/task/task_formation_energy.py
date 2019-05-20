import numpy as np
import matplotlib.pyplot as plt

task_num = ['10','15','20','25','30','35']

size = 6
x = np.arange(size)

CoalitionFormation=[0.22220858529,0.36179437186,0.48873219208,0.62469060543,0.78093006912,0.99579239567]
RandomFormation=[1.64410909784,1.56718681498,4.72102580564,4.69229586257,5.25563447718,4.61413868963]
GreedyFormation=[0.82279049794,1.77712308360,2.85080762710,2.63171676747,3.59325181244,3.80554915880]
lower_bound=[0.15721296379,0.25510900299,0.34536029391,0.41614946330,0.50194378778,0.63101230674]

total_width, n = 0.8, 4
width = total_width / n
x = x - (total_width - width) / size

label = ["Lower Bound", "F3C algorithm",'Greedy formation strategy','Random formation strategy']

'''
plt.bar(x, lower_bound, width=width, label='Lower Bound')
plt.bar(x+width, CoalitionFormation, width=width,  label='F3C algorithm',tick_label = task_num)
plt.bar(x+2*width, GreedyFormation, width=width, label='Greedy formation strategy')
plt.bar(x+3*width, RandomFormation, width=width, label='Random formation strategy')
'''
plt.bar(x, lower_bound, width=width)
plt.bar(x+width, CoalitionFormation, width=width,tick_label = task_num)
plt.bar(x+2*width, GreedyFormation, width=width)
plt.bar(x+3*width, RandomFormation, width=width)

plt.ylabel(r"Energy consumption ($\times 10^{12}$)",fontsize=18)
plt.xlabel("Task number",fontsize=18)
plt.ylim(0,6.7)
plt.legend(label,fontsize=12)
plt.show()
