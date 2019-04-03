import matplotlib.pyplot as plt
import numpy as np
import math


x=[10,15,20,25,30,35]
y=[4,6,8,8,10,16]

plt.plot(x,y,'o--',label=u'Centralized algorithm running iterations',marker = 'o')


plt.ylabel(r"Average iterations time ( s )",fontsize=12)
plt.xlabel("Number of tasks",fontsize=12)

#plt.xticks([50,100,200,350,500])

plt.legend()

plt.show()