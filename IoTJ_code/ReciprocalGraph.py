#coding:utf-8
import numpy as matrix

class ReciprocalGraph:
    user_num=0
    distance_graph=None
    datarate_graph=None


    def __init__(self,user_num):
        self.user_num=user_num
        self.distance_graph=matrix.random.randint(50,300,(self.user_num,self.user_num))
        self.distance_graph=matrix.triu(self.distance_graph)#生成一个上三角形矩阵
        self.distance_graph=self.distance_graph + matrix.diag(-matrix.diag(self.distance_graph))
        self.distance_graph+=self.distance_graph.T-matrix.diag(self.distance_graph.diagonal())

        self.datarate_graph = matrix.random.randint(10, 50, (self.user_num, self.user_num))
        self.datarate_graph = self.datarate_graph-matrix.diag(matrix.diag(self.datarate_graph))

'''reciprocalgraph=ReciprocalGraph(10)
print(reciprocalgraph.datarate_graph)'''
