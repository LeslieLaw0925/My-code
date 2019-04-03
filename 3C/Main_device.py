import threading
import Execute_device

device = threading.Thread(target=Execute_device.execute,name='device.execute')  # 线程对象.
device.start()