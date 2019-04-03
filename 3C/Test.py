import Comparison
import copy
'''
def f2(n, m, output):
    if n == 0:
        print(output)
    else:
        if m>1:
            f2(n, m-1, copy.deepcopy(output))
        if m <= n:
            output.append(m)
            f2(n-m, m, copy.deepcopy(output))


f2(10,2,[])

'''
content_size=11;N=4
partition=[0 for i in range(0,N)]
partitions=[]

def Content_partition(content_size, computing_number, partition,partitions,N):
    if content_size == 0 and computing_number == N:
        partition=sorted(partition)
        if partition not in partitions:
            partitions.append(partition)

    elif content_size >0 and computing_number < N:
        for i in range(1, content_size + 1):
            for j in range(computing_number, N):
                partition[j] = i
                Content_partition(content_size-i, computing_number+1, copy.deepcopy(partition),partitions,N)

#Content_partition(content_size, 0, partition,partitions,N)
Comparison.Content_partition(content_size, 0, partition,N,partitions)
print(partitions)
