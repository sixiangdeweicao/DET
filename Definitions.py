#!/usr/bin/python3.6
# encoding:utf-8
from copy import deepcopy
import math


class Stack(object):
    """
    栈类(DS的数据类型)
    """
    
    def __init__(self):
        self.stack = []

    def push(self, v):
        self.stack.append(v)

    def pop(self):
        if self.stack:
            return self.stack.pop(-1)
        else:
            raise LookupError('Stack is empty!')

    def is_empty(self):
        return bool(self.stack)

    def top(self):
        if self.stack:
            return self.stack[-1]
        else:
            raise LookupError('Stack is empty!')

    def find(self, v):
        return v in self.stack

class TreeNode:
    '''
    空间树的节点
    '''
    global_node_id=0
    def __init__(self,iplist,_partent=None):
        if _partent==None:
            self.level=1
        else:
            self.level=_partent.level+1
        self.iplist=iplist    # 存放ipv6种子地址向量
        self.parent=_partent
        self.childs=[]
        TreeNode.global_node_id+=1
        self.node_id=TreeNode.global_node_id #节点编号
        self.diff_delta = 0    #分裂点的维度
        self.DS=Stack()
        self.TS=[]    # 地址向量列表，每个成员代表一个被Expand的地址向量，
                      # 被Expand的维度上值为-1
        self.SS=set() # 扫描过的IPv6地址字符串集合
        self.NDA=0    # 命中个数
        self.AAD=0.0  # 命中比例
        self.last_pop=0 #记录DS上次弹出的维度（从1开始）
        self.last_pop_value=0 # 记录DS上一次弹出的值


    def isLeaf(self):
        return self.childs==[]
    
    def Steady(self,delta):
        """
        判断结点中的所有向量序列是否在维度delta上有相同值

        Args：
            delta：待判断维度

        Return：
            same：结点中向量序列在delta维度上熵为0时为True
        """
        same=True
        l=len(self.iplist)
        if l==0:
            print("the node {}  iplist has no seeds".format(self.global_node_id))
            exit()
        else:
            v1=self.iplist[0]
            for v2 in self.iplist:
                if v1[delta-1]!=v2[delta-1]:
                    same=False
                    break
        return same
    

    # 计算每一个维度上的熵值
    def get_entropy(self,i):
        info_d={} # 统计每个维度频率，保存在字典中。eg:('1'.2)
        for ip in self.iplist:
            if ip[i] in info_d:
                info_d[ip[i]]=info_d[ip[i]]+1
            else:
                info_d[ip[i]]=1
        entropy=0.0
        p=0.0
        size=len(self.iplist)
        if size==0:
            exit()
        for key in info_d:
            p=float(info_d[key])/size
            entropy=entropy+(-p*math.log(p))
        return entropy


    # 找出合适的分裂点(返回值为维度值，纬度值减一取相应的值))：熵值不为零，并且上至最小
    def get_splitP(self,delta):
        best_entropy,best_postion=float("Inf"),-2  
        for i in range(int(128/math.log(delta,2))):
            entropy=self.get_entropy(i)
            if entropy==0:
                continue
            else:
                if best_entropy>entropy:
                        best_entropy=entropy
                        best_postion=i
        return best_postion+1


    def ExpandTS(self, delta):
        """
        对结点的TS做Expand操作

        Args：
            delta：当前需要Expand的维度
        """
        if self.TS==[]: # 叶结点的TS初始为对应的地址向量子序列
            for ip in self.iplist:
                self.TS.append(deepcopy(ip))
        self.last_pop=delta

        for v in self.TS:
            v[delta-1]=-1

        # 删除TS中重复的成员
        self.TS = list(set([tuple(v) for v in self.TS]))
        self.TS = [list(v) for v in self.TS]


    def  OutputNode(self):
        """
        输出一个结点的信息

        Args:
            node:当前结点
            V：地址向量序列
        """

        if self.diff_delta == 0:
            print('[leaf]', end = ' ')
        print('Node ID: ',self.node_id)
        print('[+]{} Address(es):'.format(len(self.iplist)))
        for i in self.iplist:
            print(i)
        if self.diff_delta != 0:
            print('[+]Lowest variable dim:%d' % self.diff_delta) 
        print('[+]Parent:', end = ' ')
        if self.parent == None:
            print('None')
        else:
            print(self.parent.node_id)
        print('[+]Childs:', end = ' ')
        if self.childs == []:
            print('None')
        else:
            for child in self.childs:
                print(child.node_id, end = ' ')
            print()
        print('[+]DS:')
        print(self.DS.stack)
        print('[+]TS:')
        if self.TS == []:
            print('None')
        else:
            for v in self.TS:
                print(v)
        print('[+]SS:')
        if self.SS == []:
            print('None')
        else:
            for v in self.SS:
                print(v)
        print('[+]NDA:', self.NDA)
        print('\n')

def Intersection(l1,l2):
    '''
    计算两个列表的重复元素
    '''
    intersection=[v for v in l1 if v in l2]
    return intersection