import threading
import Execute_device
import Execute_formation_device

device = threading.Thread(target=Execute_device.execute,name='device.execute')  # 线程对象.
device.start()

'''
formation_device = threading.Thread(target=Execute_formation_device.execute,name='formation_device.execute')  # 线程对象.
formation_device.start()
'''