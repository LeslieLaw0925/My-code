import numpy as np
import matplotlib.pyplot as plt

device_num = ['70','80','90','100','120','150']

size = 6
x = np.arange(size)

Non_cooperation=[3.27065640202,2.94934758050,3.05939977166,2.32422598880,2.24631100112,3.17955029209]
CoalitionFormation=[1.13542257721,1.11485511483,1.07587221813,1.05431083380,1.03653871085,1.00359389008]
overlap_BruteGreedy=[0.95296679676,0.95305652017,0.95064636370,0.94722627501,0.93845083518,0.92469792682]
non_overlap_BruteGreedy=[1.20821811609,1.17159134365,1.12423347342,1.08063412691,1.07542669398,1.02935607229]
#range_greedy=[3.04616961458,3.02184063759,2.70147669315,2.30390022337,2.28750783318,3.09924914622]
lower_bound=[0.62414521551,0.62414521551,0.62255717427,0.62255717427,0.61570796432,0.60062269226]

total_width, n = 0.8, 5
width = total_width / n
x = x - (total_width - width) / size

plt.bar(x, lower_bound, width=width, label='Lower Bound')
plt.bar(x+width, overlap_BruteGreedy, width=width, label='Overlapping Brute Greedy strategy')
plt.bar(x+2*width, CoalitionFormation, width=width,  label='F3C algorithm',tick_label = device_num)
plt.bar(x+3*width, non_overlap_BruteGreedy, width=width, label='Non-overlapping Brute Greedy strategy')
#plt.bar(x+4*width, range_greedy, width=width, label='Range Greedy strategy')
plt.bar(x+4*width, Non_cooperation, width=width, label='Non-cooperation strategy')

plt.ylabel(r"Energy consumption ($\times 10^{11}$)",fontsize=12)
plt.xlabel("Fog device number",fontsize=12)
plt.ylim(0,5)
plt.legend()
plt.show()

