#coding:utf-8
import random as rand
import math
from Content import Content
import networkx as nx
import User
import MC_graph
import copy
import re

class Task:
    '''define a task'''
    task_range=500 # 任务与设备的可达通信范围
    output_ratio = 0.5

    def __init__(self,contents,id):
        self.task_id=id
        self.processing_density = rand.randint(1000,3000)  # cycles per bit
        self.x_axis=rand.uniform(0,500)
        self.y_axis=rand.uniform(0,500)
        self.content=contents[rand.randint(0,Content.content_num-1)]
        self.require_computing_resource = self.processing_density * self.content.input_size  # the number of CPU cycles in execution device
        self.output_block_num = int(self.content.input_block_num* self.output_ratio)  # 任务输出大小
        self.coalition_history = []
        self.avalible_users = []
        self.caching_users = []
        self.user_distances = []
        self.current_avalible_users = [] #用于CF
        self.current_caching_users = [] #用于CF

    def initilize(self):
        self.current_avalible_users .clear()
        self.current_caching_users.clear()
        self.current_flowdict = None
        self.current_mc_graph = None

    def setTimeWeight(self,time_weight):
        # 时间和能量的权重
        self.weighting_time = time_weight
        self.weighting_energy = 1 - self.weighting_time

    def setAvalibaleUsers(self,users):
        for user in users:
            distance = math.sqrt(math.pow((self.x_axis - user.x_axis), 2) + math.pow((self.y_axis - user.y_axis), 2))
            if distance < Task.task_range:
                self.avalible_users.append(user.user_id)
                self.user_distances.append(distance)
        quicksort(self.user_distances,self.avalible_users,0,len(self.avalible_users)-1,users) #根据user的蜂窝网下行链路从大到小排序


    def setCachingUsers(self,users):
        for user_id in self.avalible_users:
            if users[user_id].cached_content[self.content.content_id]==1:
                self.caching_users.append(user_id)


    def Non_cooperation_initialize(self,joined_users,users):
        min_cost = 0
        min_cost_userid = -1

        for user_id in self.avalible_users:
            if user_id in joined_users:
                continue

            user = users[user_id]
            content_size = self.output_block_num*self.content.block_size

            computing_cost = user.ComputingCost(content_size, self)
            output_cost = user.OutputCost(user, content_size)
            total_cost = computing_cost + output_cost[0]

            if user_id not in self.caching_users:
                downloading_cost = user.DownloadingCost(content_size)
                total_cost += downloading_cost

            if min_cost == 0 or total_cost < min_cost:
                min_cost = total_cost
                min_cost_userid = user_id


        joined_users.append(min_cost_userid)

        if min_cost_userid in self.caching_users:
            self.current_caching_users.append(min_cost_userid)

        self.current_avalible_users.append(min_cost_userid)


        mc_graph = MC_graph.createMCgraph(self, self.current_caching_users, self.current_avalible_users, users)
        current_flowDict = nx.network_simplex(mc_graph, demand='demand', capacity='capacity', weight='weight')

        self.current_flowdict=copy.deepcopy(current_flowDict)
        self.current_mc_graph=copy.deepcopy(mc_graph)

        users[min_cost_userid].current_task_id=self.task_id

        # 记录每个task已经组过的coalition及其组成情况
        self.record_UserHistory(self.current_avalible_users)

    def initializeCoalition(self,joined_users,users):
        caching_members = []
        avalible_members = []
        min_cost = 50*User.User.exponent

        for avalible_member_id in self.avalible_users:
            if avalible_member_id in joined_users:
                continue
            avalible_members.append(avalible_member_id)
            if avalible_member_id in self.caching_users:
                caching_members.append(avalible_member_id)

            mc_graph = MC_graph.createMCgraph(self,caching_members, avalible_members,users)
            current_flowDict = nx.network_simplex(mc_graph, demand='demand', capacity='capacity', weight='weight')

            current_cost = current_flowDict[0]

            if current_cost >= min_cost:
                avalible_members.remove(avalible_member_id)
                if avalible_member_id in caching_members:
                    caching_members.remove(avalible_member_id)
            else:
                joined_users.append(avalible_member_id)
                min_cost = current_cost
                self.current_flowdict = copy.deepcopy(current_flowDict)
                self.current_mc_graph = copy.deepcopy(mc_graph)

        #去掉没有流量通过的边和相应的结点
        self.removeUnused(joined_users,users,avalible_members)

    def removeUnused(self,joined_users,users,avalible_members):
        modified_caching_members=[]
        modified_avalible_members=[]
        if self.current_mc_graph==None or self.current_flowdict ==None:
            return
        min_cost, flowdict=self.current_flowdict
        residual_flowdict=sorted([(u, v) for u in flowdict for v in flowdict[u] if flowdict[u][v] > 0])
        #print('current_min_cost is',min_cost)
        #print('residual_flowdict is',residual_flowdict)

       #将没有流量通过的边去掉
        for u,v in residual_flowdict:
            u_id = re.sub('\D','', u)
            v_id = re.sub('\D','', v)
            u_function = u.replace(u_id,'')
            v_function = v.replace(v_id, '')
            flow_size = flowdict[u][v]

            #记录每个参与到coalition的user的花费
            if u_function=='caching' and v_function=='computing':
                caching_id=int(u_id)
                computing_id=int(v_id)
                #if caching_id!=computing_id:
                users[caching_id].current_cost+=self.current_mc_graph[u][v]['caching_user_cost']*flow_size
                users[computing_id].current_cost+=self.current_mc_graph[u][v]['computing_user_cost']*flow_size
            elif u_function=='IOTplatform' and v_function=='computing':
                computing_id = int(v_id)
                users[computing_id].current_cost += self.current_mc_graph[u][v]['computing_user_cost']*flow_size
            elif u_function=='computing' and v_function=='relaying':
                computing_id = int(u_id)
                relaying_id = int(v_id)
                #if computing_id!=relaying_id:
                users[computing_id].current_cost += self.current_mc_graph[u][v]['computing_user_cost'] * flow_size
                users[relaying_id].current_cost += self.current_mc_graph[u][v]['relaying_user_cost'] * flow_size

            if u_id != '':
                user_id=int(u_id)
                if user_id not in modified_avalible_members:
                    modified_avalible_members.append(user_id)
                    if u_function=='caching':
                    #if user_id not in modified_caching_members and user_id in self.caching_users:
                        modified_caching_members.append(user_id)

            if v_id != '':
                user_id=int(v_id)
                if user_id not in modified_avalible_members:
                    modified_avalible_members.append(user_id)
                    if v_function == 'caching':
                    #if user_id not in modified_caching_members and user_id in self.caching_users:
                        modified_caching_members.append(user_id)

        # 将没有流量通过的结点去掉
        for user_id in avalible_members:
            if user_id not in modified_avalible_members and user_id in joined_users:
                joined_users.remove(user_id)
                users[user_id].current_cost=0

        mc_graph=MC_graph.createMCgraph(self, modified_caching_members, modified_avalible_members,users)
        modified_flowdict=nx.network_simplex(mc_graph, demand='demand', capacity='capacity', weight='weight')

        #记录task当前的coalition状况
        self.current_flowdict = copy.deepcopy(modified_flowdict)
        self.current_mc_graph = copy.deepcopy(mc_graph)

        for member_id in modified_avalible_members:
            self.current_avalible_users.append(member_id)

        for member_id in modified_caching_members:
            self.current_caching_users.append(member_id)

        for user_id in modified_avalible_members:
            users[user_id].current_task_id=self.task_id


        #记录每个task已经组过的coalition及其组成情况
        self.record_UserHistory(modified_avalible_members)

    def record_UserHistory(self,modified_avalible_members):
        coalition_members_id=[]
        for user_id in modified_avalible_members:
            coalition_members_id.append(user_id)

        user_history=sorted(tuple(coalition_members_id))
        #print('user history is',user_history)

        self.coalition_history.append(user_history)

    def ifCoalitionExist(self,coalition_members):
        coalition_members_id = []

        for user_id in coalition_members:
            coalition_members_id.append(user_id)

        coalition_tuple=sorted(tuple(coalition_members_id))

        for history_coalition in self.coalition_history:
            if history_coalition==coalition_tuple:
                return True

        return False

def partition(distances,avalible_users,low,high,users): #根据user的蜂窝网下行链路从大到小排序
    i = low;j = high;key = users[avalible_users[i]].download_cellular_data_rate #distances[i]
    while i < j:
        while users[avalible_users[j]].download_cellular_data_rate <= key and i < j:
            j -= 1
        avalible_users[i], avalible_users[j] = avalible_users[j], avalible_users[i]
        distances[i], distances[j] = distances[j], distances[i]

        while users[avalible_users[i]].download_cellular_data_rate >= key and i < j:
            i += 1
        avalible_users[i], avalible_users[j] = avalible_users[j], avalible_users[i]
        distances[i], distances[j] = distances[j], distances[i]
    return i

def quicksort(distances,avalible_users,low,high,users): #根据user的蜂窝网下行链路从大到小排序
    if low<high:
        quicksort(distances,avalible_users,low,partition(distances,avalible_users,low,high,users)-1,users)
        quicksort(distances,avalible_users,partition(distances,avalible_users,low,high,users)+1,high,users)