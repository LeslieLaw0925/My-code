import matplotlib.pyplot as plt

# delay performance
# weight of delay=0
usernum = [50,100,200,350,500]

plt.xlabel("Number of devices")
plt.ylabel("Signaling overhead")

plt.ylim(2000,270000)
plt.xticks([50,100,150,200,250,300, 350,400,450,500])
plt.xlim(50,500)

cen_overheads=[2486,9836,39184,120026,245208]

plt.plot(usernum,cen_overheads,'oy-.',label=u'Centralized algorithm signal overhead')
plt.legend()

decen_overheads=[2123,7169,29782,91002,181274]

plt.plot(usernum,decen_overheads,'ok--',label=u'Decentralized algorithm signal overhead')
plt.legend()

plt.show()