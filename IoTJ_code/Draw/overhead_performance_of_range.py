import matplotlib.pyplot as plt
import numpy as np

# delay performance
# weight of delay=0
user_ranges = [0, 50, 150, 350, 500]

plt.xlabel("Scales of user access range")
plt.ylabel("Overhead performance")

plt.xlim(user_ranges[0],user_ranges[len(user_ranges)-1])
plt.ylim(2.5,3.2)


cen_overheads=[3.046940,2.880432,2.823762,2.907373,2.947783]

plt.plot(user_ranges,cen_overheads,'oy-.',label=u'Centralized algorithm overhead performance')
plt.legend()

decen_overheads=[3.041928,2.870745,2.774759,2.756574,2.750887]

plt.plot(user_ranges,decen_overheads,'ok--',label=u'decentralized algorithm overhead performance')
plt.legend()

plt.show()