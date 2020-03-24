from Definitions import Stack,TreeNode
from AddrsToSeq import AddrVecList,InputAddrs
import math
from copy import deepcopy

'''
使用DHC 算法成成一颗空间树
'''

lamada=128

def SpaceTreeGen(IPS, delta=16,beta=16):
    '''
    空间树生成

    Args:
        delta:基数
        beta:叶子结点中地址数量的上限

    Return：
        root：空间树的根结点
    '''
    root=TreeNode(IPS)
    DHC(root,beta,delta)

    return root
    
def DHC(node,beta,delta):
    '''
    层次聚类算法

    Args；
        node：当前待聚类的结点
        beta：叶结点中向量个数上限
        delta:基数
    '''
    vecnum=len(node.iplist)
    if vecnum<=beta:
        return
    # 记录当前节点所有向量中不为零的熵值最小的值所在的维度
    best_position=node.get_splitP(delta)
    if best_position==-1:
        return

    node.diff_delta=best_position
    dic_key_ips=SplitVecSeq(node,best_position)
    for key in dic_key_ips:
        new_node=TreeNode(dic_key_ips[key],_partent=node)
        node.childs.append(new_node)
    for child in node.childs:
        DHC(child,beta,delta)

        

def SplitVecSeq(node,best_position):
    '''
    将node.iplist分割成不同的list
    返回字典形式 {"1","{ip1,ip2}}"}
    '''
    dic_key_ips={}
    for ip in node.iplist:
        if ip[best_position-1] in dic_key_ips:
            dic_key_ips[ip[best_position-1]].append(ip)
        else:
            dic_key_ips[ip[best_position-1]]=[ip]
    return dic_key_ips


def OutputSpaceTree(root):
    """
    层次遍历输出空间树

    Args：
        root：空间树的根结点
    """

    print('******LEVEL 1******')
    childs = root.childs
    root.OutputNode()
    # OutputNode(root, V)
    level = 2
    while childs != []:
        print('******LEVEL %d******' % level)
        while childs != [] and childs[0].level == level:
            child = childs.pop(0)
            childs.extend(child.childs)
            child.OutputNode()
            # OutputNode(child, V)
        level += 1

if __name__ == "__main__":
    IPS=InputAddrs(input="data1.csv")
    root=SpaceTreeGen(IPS,16,16)
    OutputSpaceTree(root)
