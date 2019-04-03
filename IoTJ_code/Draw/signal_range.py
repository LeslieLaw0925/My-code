import matplotlib.pyplot as plt
import numpy as np

# delay performance
# weight of delay=0
user_ranges = [50, 150, 350, 500]

plt.xlabel("Scales of D2D range")
plt.ylabel("Signaling overhead")

plt.ylim(1000,270000)
plt.xticks([50,100, 150,200,250, 300,350, 400,450,500])
plt.xlim(user_ranges[0],user_ranges[len(user_ranges)-1])

cen_overheads=[7982,53984,186778,244076]

plt.plot(user_ranges,cen_overheads,'oy-.',label=u'Centralized algorithm signal overhead')
plt.legend()

decen_overheads=[6344,46704,149054,192364]

plt.plot(user_ranges,decen_overheads,'ok--',label=u'Decentralized algorithm signal overhead')
plt.legend()

plt.show()