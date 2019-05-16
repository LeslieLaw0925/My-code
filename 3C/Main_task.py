import threading
import Execute_task
import Execute_formation_task

device = threading.Thread(target=Execute_task.execute,name='device.execute')  # 线程对象.
device.start()

'''

formation_task = threading.Thread(target=Execute_formation_task.execute,name='formation_task.execute')  # 线程对象.
formation_task.start()
'''