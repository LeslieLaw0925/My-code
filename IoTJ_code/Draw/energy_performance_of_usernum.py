import matplotlib.pyplot as plt
import numpy as np

# delay performance
# weight of delay=0
user_num = [50,100,200,350,500]

plt.xlabel("Number of devices")
plt.ylabel("Energy performance")

plt.xlim(user_num[0],user_num[len(user_num)-1])
plt.ylim(0.12,0.13)


cen_overheads=[0.128582,0.127817,0.127671,0.125299,0.125019]

plt.plot(user_num,cen_overheads,'oy-.',label=u'Centralized algorithm energy performance')
plt.legend()

decen_overheads=[0.128283,0.127518,0.127372,0.125000,0.124720]

plt.plot(user_num,decen_overheads,'ok--',label=u'decentralized algorithm energy performance')
plt.legend()

plt.show()