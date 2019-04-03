import numpy as np
import matplotlib.pyplot as plt

device_num = ['100','200','300','400','500']

size = 5
x = np.arange(size)

Non_cooperation_saving_ratio=[52.580675,83.391178,99,91.398806,81.072336]
BruteGreedy_saving_ratio=[31.616811,29.179118,53.793101,34.091183,35.819173]
Random_cooperation_saving_ratio=[100,100,100,100,100]
CoalitionFormation_saving_ratio=[31.545694,27.631237,48.907296,30.353996,27.093874]

total_width, n = 0.8, 5
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, Random_cooperation_saving_ratio, width=width, label='Random cooperation strategy')
plt.bar(x+width, Non_cooperation_saving_ratio, width=width,  label='Non-cooperation strategy')
plt.bar(x+2*width, BruteGreedy_saving_ratio, width=width, label='Brute Greedy strategy',tick_label = device_num)
plt.bar(x+3*width, CoalitionFormation_saving_ratio, width=width, label='F3C algorithm')

plt.ylabel("Energy consumption ratio (%)",fontsize=12)
plt.xlabel("Fog device number",fontsize=12)
plt.ylim(0,150)
plt.legend()
plt.show()

