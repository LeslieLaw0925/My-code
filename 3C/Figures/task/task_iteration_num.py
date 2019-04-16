import matplotlib.pyplot as plt
import numpy as np
import math


x=[10,15,20,25,30,35]
y=[18,31,41,80,100,135]

plt.plot(x,y,'o--',marker = 'o')


plt.ylabel(r"Average number of permitted operations",fontsize=15)
plt.xlabel("Task number",fontsize=15)

#plt.xticks([50,100,200,350,500])

plt.legend()

plt.show()