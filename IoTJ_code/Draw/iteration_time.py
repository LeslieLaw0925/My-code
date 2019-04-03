import matplotlib.pyplot as plt
import numpy as np
import math


x=[50,100,200,350,500]
y=[6.016970,56.816578,750.380993,5618.173838,18989.766359]
z=[208.263230,1112.014484,4056.564132,11878.468971,22246.059018]

# iteration
'''
y1=[0.78,
3.84,
32.22,
341.7,
2126.16,
6880.74]
'''
y1=[] #centralized
y2=[] #decentralized

for i in range(0,len(x)):
    y1.append(y[i])
    y2.append(z[i])


plt.plot(x,y1,'ro--',label=u'Centralized algorithm running iterations')
plt.plot(x,y2,'c-.',marker = 'o' ,label=u'Decentralized algorithm running iterations')

plt.ylabel(r"Average iterations time ( ms )",fontsize=12)
plt.xlabel("Number of devices",fontsize=12)

plt.xticks([50,100,200,350,500])

plt.xlim(50,500)

plt.legend()

plt.show()