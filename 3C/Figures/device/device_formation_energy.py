import numpy as np
import matplotlib.pyplot as plt

device_num = ['80', '100', '200', '300', '400', '500']

size = 6
x = np.arange(size)

CoalitionFormation=[0.081801408704,0.078439298774,0.072432065808,0.070119694884,0.069757779826,0.069149191092]
RandomFormation=[0.437956763296,0.463330445871,0.419525012713,0.403394750536,0.350366507907,0.7]
GreedyFormation=[0.220828564202,0.243416479961,0.326805981700,0.348366141718,0.205039179231,0.506266382644]
lower_bound=[0.073006687378,0.071929813024,0.070401705411,0.068059897263,0.068059897263,0.068014908982]

label = ["Lower Bound", "F3C algorithm",'Greedy formation strategy','Random formation strategy']

total_width, n = 0.8, 4
width = total_width / n
x = x - (total_width - width) / size
'''
plt.bar(x, lower_bound, width=width, label='Lower Bound')
plt.bar(x+width, CoalitionFormation, width=width,  label='F3C algorithm',tick_label = device_num)
plt.bar(x+2*width, GreedyFormation, width=width, label='Greedy formation strategy')
plt.bar(x+3*width, RandomFormation, width=width, label='Random formation strategy')
'''
plt.bar(x, lower_bound, width=width)
plt.bar(x+width, CoalitionFormation, width=width,tick_label = device_num)
plt.bar(x+2*width, GreedyFormation, width=width)
plt.bar(x+3*width, RandomFormation, width=width)

plt.ylabel(r"Energy consumption ($\times 10^{12}$)",fontsize=18)
plt.xlabel("Fog device number",fontsize=18)
plt.ylim(0,1.0)
plt.legend(label,fontsize=12)
plt.show()

