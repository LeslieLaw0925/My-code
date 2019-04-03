import matplotlib.pyplot as plt
import numpy as np

# delay performance
# weight of delay=0
user_ranges = [0, 50, 150, 350, 500]

plt.xlabel("Scales of user access range")
plt.ylabel("Energy performance")

plt.xlim(user_ranges[0],user_ranges[len(user_ranges)-1])
plt.ylim(0.13,0.15)


cen_overheads=[0.142113,0.139306,0.134172,0.132357,0.131986]

plt.plot(user_ranges,cen_overheads,'oy-.',label=u'Centralized algorithm energy performance')
plt.legend()

decen_overheads=[0.141797,0.138990,0.133855,0.132041,0.131669]

plt.plot(user_ranges,decen_overheads,'ok--',label=u'decentralized algorithm energy performance')
plt.legend()

plt.show()