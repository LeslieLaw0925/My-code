import threading
import Execution_mwmatching

iteration_time=[10]

mwmatching = threading.Thread(target=Execution_mwmatching.execute,args=iteration_time ,name='Execution_mwmatching.execute')  # 线程对象.
mwmatching.start()