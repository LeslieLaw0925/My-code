
usernum_cen_overheads=[2493,9868,39236,119854,244325] #固定了可达距离
usernum_decen_overheads=[1800,7174,29160,90182,187077]

range_cen_overheads=[8199,55102,188366,244328]#固定了用户数
range_decen_overheads=[6393,47748,152272,189532]

def average_rate(data):
    length=len(data)
    first=data[0]
    last=data[length-1]

    return (pow(last/first,1/(length-1))-1)*100

print('centralized average signal increasing rate is %f%% under fixed D2D range'%average_rate(usernum_cen_overheads))
print('decentralized average signal increasing rate is %f%% under fixed D2D range\n'%average_rate(usernum_decen_overheads))

print('centralized average signal increasing rate is %f%% under fixed user number'%average_rate(range_cen_overheads))
print('decentralized average signal increasing rate is %f%% under fixed user number'%average_rate(range_decen_overheads))