import matplotlib.pyplot as plt
import numpy as np
import math


x=[70,80,90,100,120,150]
y=[104,98,83,67,98,115]

plt.plot(x,y,'o--',marker = 'o')


plt.ylabel(r"Average permitted operation number",fontsize=18)
plt.xlabel("Fog device number",fontsize=18)

#plt.xticks([50,100,200,350,500])

plt.legend()

plt.show()