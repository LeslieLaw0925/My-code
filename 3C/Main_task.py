import threading
import Execute_task

device = threading.Thread(target=Execute_task.execute,name='device.execute')  # 线程对象.
device.start()