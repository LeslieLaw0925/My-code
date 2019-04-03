import Execution_range
import Energy_execution_range
import Time_execution_range
import threading

'''
average_overheads=None

class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        global average_overheads
        average_overheads= Execution_range.execute(self.threadID)

# 创建新线程
thread3 = myThread(2)

# 开启线程
thread3.start()

average_overheads= Execution_range.execute(0)
print('average_overheads is:',average_overheads)
print_overhead.Performance_of_range([0,50,150,350,500], average_overheads,'average overhead')
'''

iteration_time=[10]

range = threading.Thread(target=Execution_range.execute,args=iteration_time ,name='Execution_range.execute')  # 线程对象.
range.start()

energy_range = threading.Thread(target=Energy_execution_range.execute,args=iteration_time ,name='Energy_execution_range.execute')  # 线程对象.
energy_range.start()


time_range = threading.Thread(target=Time_execution_range.execute,args=iteration_time ,name='Time_execution_range.execute')  # 线程对象.
time_range.start()
