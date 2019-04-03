import matplotlib.pyplot as plt
import numpy as np
import math


x=[100,200,300,400,500]
y=[55,57,60,67,68]

plt.plot(x,y,'o--',marker = 'o')


plt.ylabel(r"Average permitted operation number",fontsize=15)
plt.xlabel("Fog device number",fontsize=15)

#plt.xticks([50,100,200,350,500])

plt.legend()

plt.show()