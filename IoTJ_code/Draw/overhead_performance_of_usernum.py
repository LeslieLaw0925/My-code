import matplotlib.pyplot as plt

# delay performance
# weight of delay=0
usernum = [50,100,200,350,500]

plt.xlabel("Number of devices")
plt.ylabel("Overhead performance ")

plt.xlim(usernum[0],usernum[len(usernum)-1])
plt.ylim(2.5,3)


cen_overheads=[2.751875,2.741829,2.726658,2.742001,2.882951]

plt.plot(usernum,cen_overheads,'oy-.',label=u'Centralized algorithm overhead performance')
plt.legend()

decen_overheads=[2.750399,2.739923,2.718359,2.688507,2.688554]

plt.plot(usernum,decen_overheads,'ok--',label=u'decentralized algorithm overhead performance')
plt.legend()

plt.show()