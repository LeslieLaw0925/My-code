
import Execution_usernum
import Time_execution_usernum
import Energy_execution_usernum
import threading


#iteration_time=[50]
iteration_time=[10]


usernum = threading.Thread(target=Execution_usernum.execute,args=iteration_time ,name='Execution_usernum.execute')  # 线程对象.
usernum.start()

energy_usernum = threading.Thread(target=Energy_execution_usernum.execute,args=iteration_time ,name='Energy_execution_usernum.execute')  # 线程对象.
energy_usernum.start()


time_usernum = threading.Thread(target=Time_execution_usernum.execute,args=iteration_time ,name='Time_execution_usernum.execute')  # 线程对象.
time_usernum.start()
