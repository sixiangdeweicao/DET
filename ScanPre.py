#!/usr/bin/python3.6
# encoding:utf-8
from AddrsToSeq import InputAddrs
from Definitions import Stack
from DHC import SpaceTreeGen, OutputSpaceTree
from copy import deepcopy
import math
import pdb

def ScanPre(root):
    """
    动态扫描开始前的准备工作

    Args:
        root:空间树的根结点
    """

    InitializeDS(root)
    InitializeTS(root)


def InitializeDS(node, parent_stack = Stack(), beta=16):
    """
    对结点node的DS进行初始化

    Args：
        node：当前DS待初始化的结点
        parent_stack：父结点的DS            
        beta：向量每一维度的基数
    """    
    
    # pdb.set_trace()
    parent=node.parent
    stack = deepcopy(parent_stack) #注意要将父结点的DS做拷贝
    if parent !=None:
        stack.push(parent.diff_delta)

    vecDim = int(128 / math.log(beta, 2))

    for delta in range(1, vecDim + 1):        
        if node.Steady(delta) and stack.find(delta) == False:
            stack.push(delta)

    if not node.isLeaf():
        for child in node.childs:
            InitializeDS(child, stack, beta)
    else:
        for delta in range(1, vecDim + 1):
            if stack.find(delta) == False:
                stack.push(delta)
    
    node.DS = stack
    # pdb.set_trace()


def InitializeTS(node):
    """
    对所有叶结点的TS进行初始化（SS和NDA在结点创建时已被初始化）

    Args：
        node：当前TS待初始化的结点
    """

    # pdb.set_trace()

    if node.isLeaf():
        delta = node.DS.pop()
        # print(node.node_id)
        # print(delta)
        # node.last_pop = delta
        # node.last_pop_value = node.TS[delta - 1]
        # print("leaf node :{}".format(node.global_node_id))
        node.ExpandTS(delta)
    else:
        for child in node.childs:
            InitializeTS(child)    
    # pdb.set_trace()
    


if __name__ == '__main__':
    IPS=InputAddrs(input="data1.csv")
    root=SpaceTreeGen(IPS,16,16)
    ScanPre(root)
    OutputSpaceTree(root)