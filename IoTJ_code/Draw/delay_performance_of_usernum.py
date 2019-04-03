import matplotlib.pyplot as plt
import numpy as np

# delay performance
# weight of delay=0
user_num = [50,100,200,350,500]

plt.xlabel("Number of devices")
plt.ylabel("Delay performance")

plt.xlim(user_num[0],user_num[len(user_num)-1])
plt.ylim(5,6)


cen_overheads=[5.248014,5.231594,5.217435,5.300104,5.560232]

plt.plot(user_num,cen_overheads,'oy-.',label=u'Centralized algorithm energy performance')
plt.legend()

decen_overheads=[5.244813,5.227115,5.199466,5.186793,5.176212]

plt.plot(user_num,decen_overheads,'ok--',label=u'decentralized algorithm energy performance')
plt.legend()

plt.show()