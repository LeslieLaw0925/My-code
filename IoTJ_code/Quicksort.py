#coding:utf-8
import random as randomize
import User

def partition(pre_list,low,high,overheads,strategy,time_overheads,energy_overheads):
    i = low;j = high;key=overheads[i]
    while i<j:
        while overheads[j]>=key and i<j:
            j-=1
        pre_list[i], pre_list[j] = pre_list[j], pre_list[i]
        overheads[i], overheads[j] = overheads[j], overheads[i]
        strategy[i], strategy[j] = strategy[j], strategy[i]
        time_overheads[i], time_overheads[j] = time_overheads[j], time_overheads[i]
        energy_overheads[i], energy_overheads[j] = energy_overheads[j], energy_overheads[i]

        while overheads[i]<=key and i<j:
            i+=1
        pre_list[i], pre_list[j] = pre_list[j], pre_list[i]
        overheads[i], overheads[j] = overheads[j], overheads[i]
        strategy[i], strategy[j] = strategy[j], strategy[i]
        time_overheads[i], time_overheads[j] = time_overheads[j], time_overheads[i]
        energy_overheads[i], energy_overheads[j] = energy_overheads[j], energy_overheads[i]

    return i

def quicksort(pre_list,low,high,overheads,strategy,time_overheads,energy_overheads):
    if low<high:
        quicksort(pre_list,low,partition(pre_list, low, high,overheads,strategy,time_overheads,energy_overheads)-1,overheads,strategy,time_overheads,energy_overheads)
        quicksort(pre_list,partition(pre_list, low, high,overheads,strategy,time_overheads,energy_overheads)+1,high,overheads,strategy,time_overheads,energy_overheads)






