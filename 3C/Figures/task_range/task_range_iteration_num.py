import matplotlib.pyplot as plt
import numpy as np
import math


x=[100,200,300,400,500,600]
y=[95,62,57,65,59,50]

plt.plot(x,y,'o--',marker = 'o')


plt.ylabel(r"Average number of feasible operations",fontsize=12)
plt.xlabel("Task range",fontsize=12)

#plt.xticks([50,100,200,350,500])

plt.legend()

plt.show()