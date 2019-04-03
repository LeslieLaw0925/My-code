#coding:utf-8
import random as rand
import math
import numpy

class User:
    '''define User'''

    def __init__(self,user_id):
        self.user_id=user_id
        self.computation_capacity = rand.randint(1,10) * math.pow(10, 9)  # 2Ghz CPU cycles per unit time

        self.cellular_transmission_power = rand.randint(100, 600) / 1000  # 600mW
        self.cellular_receiving_power = rand.randint(100, 600) / 1000  # 600mW
        self.D2D_transmission_power = rand.randint(50, 200) / 1000  # 200mW
        self.D2D_receiving_power = rand.randint(50, 200) / 1000  # 200mW
        self.CPU_power = rand.randint(100, 600) / 1000  # 600mW

        self.CPU_energy_percycle =self.CPU_power/self.computation_capacity
        self.strategylist =[] #策略列表
        self.overheads =[] #helpers的消耗列表
        self.time_overheads=[] #helpers的时间消耗列表
        self.energy_overheads=[]
        self.preference_list=[] #user的helper排序列表
        self.most_preferred_helper_id=None

    def initialize(self):
        self.strategylist .clear()  # 策略列表
        self.overheads .clear()  # helpers的消耗列表
        self.time_overheads .clear()  # helpers的时间消耗列表
        self.energy_overheads.clear()  # helpers的能量消耗列表
        self.preference_list.clear()   #user的helper排序列表
        #self.SNR = rand.uniform(5, 50)  # dB 信噪比
        self.SNR = 50 #dB 信噪比
        self.cloud_computation_capacity = rand.uniform(1,5) * math.pow(10, 9)  # Ghz 云服务器的计算资源,存疑！！！
        self.current_load = rand.uniform(0, 0.5)  # percentage of occupied processing capacity
        self.idle_computation_capacity = (1 - self.current_load) * self.computation_capacity  # /Ghz idle computation capacity
        self.download_cellular_data_rate = rand.uniform(10,100) * math.pow(10, 6)  # /Mbps 蜂窝网下行链路
        self.upload_cellular_data_rate = self.download_cellular_data_rate * rand.uniform(0, 0.5)  # /Mbps 蜂窝网上行链路
        self.flag=0
        #self.D2D_bandwidth=rand.randint(1,50)*math.pow(10,6) #Mhz 带宽最大为50Mhz
        self.D2D_bandwidth = 50 * math.pow(10, 6) #Mhz 带宽最大为50Mhz
        self.x_axis=rand.uniform(0,500)
        self.y_axis=rand.uniform(0,500)

    def setCurrentTask(self,current_task):
        self.current_task=current_task

    def setPreferrencelist(self,user_range,users):
        #self.preference_list=[i for i in range(0,user_num)]
        for helper in users:
            if helper.user_id==self.user_id:
                self.preference_list.append(helper.user_id)
            else:
                distance = math.sqrt(math.pow((self.x_axis - helper.x_axis),2) + math.pow((self.y_axis - helper.y_axis),2))
                if distance < user_range:
                    self.preference_list.append(helper.user_id)


    def LocalExecution(self):
        print('user %d 本地处理信息如下：'% self.user_id)
        #本地处理时间
        self.localexecution_time=self.current_task.require_computing_resource/self.idle_computation_capacity
        print('user %d 本地处理的时间：%f'% (self.user_id,self.localexecution_time))
        #本地处理花费的能量
        self.localexecution_energy=self.CPU_energy_percycle*self.current_task.require_computing_resource
        print('user %d 本地处理花费的能量：%f' % (self.user_id, self.localexecution_energy))
        # 本地处理的utility
        self.local_processing_overhead=self.current_task.weighting_time*self.localexecution_time+self.current_task.weighting_energy*self.localexecution_energy
        print('user %d 本地处理的消耗：%f\n' % (self.user_id, self.local_processing_overhead))
        return [self.local_processing_overhead,self.localexecution_time,self.localexecution_energy]

    def Direct_cloud_execution(self):
        print('user %d 直接上传到云服务器处理信息如下：' % self.user_id)
        cellular_transmission_upload_time=self.current_task.input_size/self.upload_cellular_data_rate
        cellular_transmission_download_time=self.current_task.output_size/self.download_cellular_data_rate
        #蜂窝网传输时间
        cellular_transmission_time=cellular_transmission_upload_time+cellular_transmission_download_time
        print('user %d 蜂窝网传输时间：%f' % (self.user_id, cellular_transmission_time))

        # 蜂窝网传输消耗的总能量
        self.directTocloud_energy=self.cellular_transmission_power*cellular_transmission_upload_time+self.cellular_receiving_power*cellular_transmission_download_time
        print('user %d 蜂窝网传输消耗的总能量：%f' % (self.user_id, self.directTocloud_energy))

        #在云服务器处理的时间
        cloud_processing_time = self.current_task.require_computing_resource / self.cloud_computation_capacity
        print('user %d 的任务在云服务器处理的时间：%f' % (self.user_id, cloud_processing_time))

        # 蜂窝网传输的总时间
        self.directTocloud_time=cellular_transmission_time+cloud_processing_time

        # 直接上传到云处理的utility
        self.direct_cloud_execution_overhead=self.current_task.weighting_time*self.directTocloud_time+self.current_task.weighting_energy*self.directTocloud_energy
        print('user %d 的任务直接上传到云处理的消耗：%f\n' % (self.user_id, self.direct_cloud_execution_overhead))
        return  [self.direct_cloud_execution_overhead,self.directTocloud_time,self.directTocloud_energy]

    def D2D_offloaded_execution(self,offloaded_helper):
        print('user %d 上传到helper %d 处理信息如下：' % (self.user_id,offloaded_helper.user_id))
        user_D2D_datarate=self.transmission_datarate(offloaded_helper) #从源节点到迁移节点的data rate
        helper_D2D_datarate=self.receiving_datarate(offloaded_helper) #从迁移节点到源节点的data rate

        # 迁移时传输的时间
        T_transmission=self.current_task.input_size/user_D2D_datarate
        T_receiving=self.current_task.output_size/helper_D2D_datarate
        total_transmission_time=T_transmission+T_receiving
        print('user %d 到helper %d 的任务传输总时间：%f' % (self.user_id,offloaded_helper.user_id,total_transmission_time))

        # 迁移时传输耗费的能量
        energy_transmission_power=(self.D2D_transmission_power+offloaded_helper.D2D_receiving_power)*T_transmission
        energy_receiving_power=(self.D2D_receiving_power+offloaded_helper.D2D_transmission_power)*T_receiving
        total_transmission_power=energy_receiving_power+energy_transmission_power
        print('user %d 到helper %d 的任务传输总能量：%f' % (self.user_id, offloaded_helper.user_id, total_transmission_power))

        # 迁移到helper上进行处理的时间
        helper_processing_time=self.current_task.require_computing_resource/offloaded_helper.idle_computation_capacity
        print('user %d 的任务在helper %d 上处理的时间：%f' % (self.user_id, offloaded_helper.user_id, helper_processing_time))

        # 迁移到helper上进行处理消耗的能量
        helper_processing_power=offloaded_helper.CPU_energy_percycle*self.current_task.require_computing_resource
        print('user %d 的任务在helper %d 上处理消耗的能量：%f' % (self.user_id, offloaded_helper.user_id, helper_processing_power))

        user_energy=self.D2D_transmission_power*T_transmission+self.D2D_receiving_power*T_receiving
        helper_energy=offloaded_helper.D2D_receiving_power*T_transmission+offloaded_helper.D2D_transmission_power*T_receiving+helper_processing_power

        # 迁移处理的utility
        offloaded_processing_overhead=self.current_task.weighting_time*(total_transmission_time+helper_processing_time)+self.current_task.weighting_energy*(total_transmission_power+helper_processing_power)
        print('user %d 的任务迁移到helper %d 处理的开销：%f\n' % (self.user_id, offloaded_helper.user_id, offloaded_processing_overhead))

        return [offloaded_processing_overhead,total_transmission_time+helper_processing_time,total_transmission_power+helper_processing_power,user_energy,helper_energy]

    def D2D_Assisted_cloud_execution(self,offloaded_helper):
        print('user %d 通过helper %d 上传到云服务器处理信息如下：' % (self.user_id, offloaded_helper.user_id))
        user_D2D_datarate = self.transmission_datarate(offloaded_helper)  # 从源节点到迁移节点的data rate
        helper_D2D_datarate = self.receiving_datarate(offloaded_helper)  # 从迁移节点到源节点的data rate

        # 迁移时传输的时间
        T_transmission = self.current_task.input_size / user_D2D_datarate
        T_receiving = self.current_task.output_size / helper_D2D_datarate
        D2D_transmission_time = T_transmission + T_receiving
        print('user %d 的任务在helper %d 传输的总时间：%f' % (self.user_id, offloaded_helper.user_id, D2D_transmission_time))

        # 迁移时传输耗费的能量
        energy_transmission_power = (self.D2D_transmission_power + offloaded_helper.D2D_receiving_power) * T_transmission
        energy_receiving_power = (self.D2D_receiving_power + offloaded_helper.D2D_transmission_power) * T_receiving
        D2D_transmission_power = energy_receiving_power + energy_transmission_power
        print('user %d 的任务在helper %d 传输消耗的总能量：%f' % (self.user_id, offloaded_helper.user_id, D2D_transmission_power))

        #helper 上传到云服务器和结果返回接收的时间
        cellular_transmission_time=self.current_task.input_size/offloaded_helper.upload_cellular_data_rate
        cellular_receiving_time=self.current_task.output_size/offloaded_helper.download_cellular_data_rate
        cellular_time=cellular_transmission_time+cellular_receiving_time
        print('user %d 的helper %d 在云服务器间传输的时间：%f' % (self.user_id, offloaded_helper.user_id, cellular_time))

        #helper 上传到云服务器和结果返回的能量
        cellular_transmission_power=cellular_transmission_time*offloaded_helper.cellular_transmission_power+cellular_receiving_time*offloaded_helper.cellular_receiving_power
        print('user %d 的helper %d 在云服务器间传输消耗的能量：%f' % (self.user_id, offloaded_helper.user_id, cellular_transmission_power))

        #在云服务器处理的时间
        cloud_processing_time = self.current_task.require_computing_resource / self.cloud_computation_capacity
        print('user %d 的任务在云服务器上处理的时间：%f' % (self.user_id,cloud_processing_time))

        D2D_Assisted_cloud_execution_time=D2D_transmission_time+cellular_time+cloud_processing_time
        D2D_Assisted_cloud_execution_energy=D2D_transmission_power+cellular_transmission_power

        user_energy = self.D2D_transmission_power * T_transmission + self.D2D_receiving_power * T_receiving
        helper_energy = offloaded_helper.D2D_receiving_power * T_transmission + offloaded_helper.D2D_transmission_power * T_receiving + cellular_transmission_power

        D2D_assisted_cloud_execution_overhead=self.current_task.weighting_time*D2D_Assisted_cloud_execution_time+self.current_task.weighting_energy*D2D_Assisted_cloud_execution_energy
        print('user %d 借助helper %d 上传到云服务器的总消耗：%f\n' % (self.user_id,offloaded_helper.user_id,D2D_assisted_cloud_execution_overhead))

        return  [D2D_assisted_cloud_execution_overhead,D2D_Assisted_cloud_execution_time,D2D_Assisted_cloud_execution_energy,user_energy,helper_energy]

    def transmission_datarate(self,offloaded_helper):
        return  self.D2D_bandwidth * math.log2(1+math.pow(10,offloaded_helper.SNR/10))

    def receiving_datarate(self,offloaded_helper):
        datarate=self.D2D_bandwidth * math.log2(1 + math.pow(10, self.SNR / 10))
        print('data rate is between user %d and user %d is %f bit/sec'% (self.user_id,offloaded_helper.user_id,datarate))
        return datarate

    def reporting_result(self):
        probing_size=1 * 1024 * 8  #1KB的preference list信息
        core_result_size=0.5 * 1024 * 8  #0.5KB的结果

        probing_uploading_time=probing_size/self.upload_cellular_data_rate
        probing_downloading_time=core_result_size/self.download_cellular_data_rate

        probing_time=probing_uploading_time+probing_downloading_time

        probing_uploading_energy=probing_uploading_time*self.cellular_transmission_power
        probing_downloading_energy=probing_downloading_time*self.cellular_receiving_power

        probing_energy=probing_uploading_energy+probing_downloading_energy

        return [probing_time,probing_energy]


























