import numpy as np
import matplotlib.pyplot as plt

device_num = ['80', '100', '200', '300', '400', '500']

size = 6
x = np.arange(size)

CF=[42,44,48,45,46,47]
RandomFormation=[64,67,65,64,60,60]
GreedyFormation=[75,75,75,75,75,75]

total_width, n = 0.8,4
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, CF, width=width, label='F3C algorithm')
plt.bar(x+width, RandomFormation, width=width,  label='Random formation strategy',tick_label = device_num,hatch='////')
plt.bar(x+2*width, GreedyFormation, width=width, label='Greedy formation strategy strategy')


plt.ylabel("Participated device number T'",fontsize=15)
plt.xlabel("Fog device number",fontsize=15)
plt.ylim(0,100)
plt.legend()
plt.show()

