import Execute_device
import threading
import Execute_task_range


task_range = threading.Thread(target=Execute_task_range.execute, name='task_range.execute')  # 线程对象.
task_range.start()

