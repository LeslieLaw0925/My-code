#coding:utf-8
import random as rand

class Task:
    '''define a task'''

    def __init__(self):
        self.input_size = rand.randint(500, 2000)* 1024 * 8  # KB 任务输入大小
        self.output_size = self.input_size * (rand.uniform(0, 0.2))  # 任务输出大小
        self.processing_density = rand.randint(1000,3000)  # cycles per bit
        self.require_computing_resource = self.processing_density * self.input_size # the number of CPU cycles in execution device

    def setTimeWeight(self,time_weight):
        # 时间和能量的权重
        self.weighting_time = time_weight
        self.weighting_energy = 1 - self.weighting_time

