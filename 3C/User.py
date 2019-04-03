#coding:utf-8
import random as rand
import math
from Content import Content
import numpy as np
from Task import Task

class User:
    '''define User'''
    exponent = math.pow(10, 10)

    def __init__(self,user_id):
        self.user_id=user_id
        self.computation_capacity = rand.randint(1,10) * math.pow(10, 9)  # 2Ghz CPU cycles per unit time

        self.cellular_transmission_power = 600 / 1000  # 600mW
        self.cellular_receiving_power = 600 / 1000  # 600mW
        self.D2D_transmission_power = 200 / 1000  # 200mW
        self.D2D_receiving_power = 200 / 1000  # 200mW
        self.CPU_power = 600 / 1000  # 600mW

        self.CPU_energy_percycle =self.CPU_power/self.computation_capacity
        self.avalibleCooperators=[] #user的可达范围内的helper
        self.avalibleTasks=[] #user的可达范围内的task
        self.most_preferred_helper_id=None
        self.cached_content=np.random.randint(0,2,Content.content_num) #当前设备缓存的所有content
        self.current_task_id = -1

    def initialize(self):
        self.avalibleCooperators.clear()   #user的可达范围内的helper
        self.SNR = rand.uniform(5, 50)  # dB 信噪比
        self.cloud_computation_capacity = rand.randint(3,5) * math.pow(10, 9)  # Ghz 云服务器的计算资源,存疑！！！
        self.current_load = rand.uniform(0, 0.5)  # percentage of occupied processing capacity
        self.idle_computation_capacity = (1 - self.current_load) * self.computation_capacity  # /Ghz idle computation capacity
        self.residual_CPU=self.idle_computation_capacity #用于解最优值
        self.download_cellular_data_rate = rand.uniform(5,20) * math.pow(10, 6)  # /Mbps 蜂窝网下行链路
        self.upload_cellular_data_rate = self.download_cellular_data_rate * rand.uniform(0, 0.5)  # /Mbps 蜂窝网上行链路
        self.flag=0
        self.D2D_bandwidth=rand.randint(1,5)*math.pow(10,6) #Mhz 带宽最大为20Mhz
        self.x_axis=rand.uniform(0,500)
        self.y_axis=rand.uniform(0,500)
        self.current_cost = 0


    def InputCost(self,caching_user,input_size):
        if caching_user.user_id==self.user_id:
            return [0,0,0]
        user_D2D_datarate = self.transmission_datarate(caching_user)  # 从源节点到迁移节点的data rate
        # 迁移时传输的时间
        T_transmission = input_size / user_D2D_datarate

        # 迁移时传输耗费的能量
        caching_user_cost=int(caching_user.D2D_transmission_power* T_transmission*User.exponent*(1/Task.output_ratio))
        current_user_cost=int(self.D2D_receiving_power * T_transmission*User.exponent*(1/Task.output_ratio))
        inputCost=caching_user_cost+current_user_cost

        return [inputCost,current_user_cost,caching_user_cost]

    def DownloadingCost(self,download_size):
        downloadingCost=download_size/self.download_cellular_data_rate * self.cellular_receiving_power

        return int(downloadingCost*User.exponent*(1/Task.output_ratio))


    def ComputingCost(self,computing_size,task):
        computingCost=computing_size*task.processing_density*self.CPU_energy_percycle

        return int(computingCost*(1/Task.output_ratio)*User.exponent)

    def OutputCost(self,relay_user,output_size):
        if relay_user.user_id==self.user_id:
            outputCost = int((output_size / self.upload_cellular_data_rate) * self.cellular_transmission_power*User.exponent)
            return [outputCost,0,outputCost]

        user_D2D_datarate = self.transmission_datarate(relay_user)  # 从源节点到迁移节点的data rate
        # output传输的时间
        T_transmission = output_size / user_D2D_datarate

        # ouput传输耗费的能量
        relay_user_cost=int((relay_user.D2D_receiving_power* T_transmission + output_size / relay_user.upload_cellular_data_rate * relay_user.cellular_transmission_power)*User.exponent)
        current_user_cost=int(self.D2D_transmission_power*T_transmission*User.exponent)
        outputCost = relay_user_cost+current_user_cost

        return [outputCost,current_user_cost,relay_user_cost]

    def setAvalibleCooperators(self, user_range, users):
        for helper in users:
            if helper.user_id == self.user_id:
                self.avalibleCooperators.append(helper.user_id)
            else:
                distance = math.sqrt(
                    math.pow((self.x_axis - helper.x_axis), 2) + math.pow((self.y_axis - helper.y_axis), 2))
                if distance < user_range:
                    self.avalibleCooperators.append(helper.user_id)

    def transmission_datarate(self, caching_user):
        return self.D2D_bandwidth * math.log2(1 + math.pow(10, caching_user.SNR / 10))





























