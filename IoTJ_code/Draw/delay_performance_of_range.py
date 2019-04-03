import matplotlib.pyplot as plt
import numpy as np

# delay performance
# weight of delay=0
user_ranges = [0, 50, 150, 350, 500]

plt.xlabel("Scales of user access range")
plt.ylabel("Delay performance")

plt.xlim(user_ranges[0],user_ranges[len(user_ranges)-1])
plt.ylim(5,6)


cen_overheads=[5.823202,5.615459,5.547590,5.689402,5.768026]

plt.plot(user_ranges,cen_overheads,'oy-.',label=u'Centralized algorithm energy performance')
plt.legend()

decen_overheads=[5.814609,5.595302,5.448254,5.397470,5.391710]

plt.plot(user_ranges,decen_overheads,'ok--',label=u'decentralized algorithm energy performance')
plt.legend()

plt.show()