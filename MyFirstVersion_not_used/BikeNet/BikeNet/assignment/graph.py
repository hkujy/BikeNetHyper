"""
    contain the graph class
"""
import numpy as np


class edge_a:
    def __init__(self, edge_info):
        self.id = edge_info[0]
        self.pointer = vertex_a(edge_info[1])
        self.pointee = vertex_a(edge_info[2])
        self.fft = float(edge_info[3])  # fre flow travel time
        self.capacity1 = float(edge_info[4])
        self.alpha = float(edge_info[5])
        self.beta = float(edge_info[6])
        self.cost = float('inf')
        self.volume1 = 0 # flow
        self.volume2 = 0
        self.capacity2 = float(edge_info[7].strip())
    # calculate the weight by BPR function:
    def cal_weight1(self,volume1,volume2,_label_lane):
        """
            BPR_function
        """
        # _label_lane==1 means this lane is selected and will be devided into exclusive bike lane and motor lane
        if _label_lane==1:
            self.cost = self.fft*(1+self.alpha*np.power(volume1/self.capacity1, self.beta))
        else:
            self.cost = self.fft*(1+self.alpha*np.power((volume1+volume2)/(self.capacity1+self.capacity2),self.beta))
        return self.cost

    def __eq__(self, other):
        """
            compare two edges are equal or not 
            not clear where to use
        """
        if isinstance(other, self.__class__):
            return (self.pointer.id == other.pointer.id) and (self.pointee.id == other.pointee.id)
        else:
            return False


class vertex_a:
    def __init__(self, node_id):
        self.id = node_id
        self.tails = []
        self.heads = []
        self.prev = None
        self.potential = float('inf')

    def __cmp__(self, other):
        """
            compare the label of two links 
            used in the shortest path
        """
        return __cmp__(self.potential, other.potential)


class network_a:
    """
        use "set" data type, which can not be assessed by index
    """
    def __init__(self, netname):
        self.name = netname
        self.edge_id_set = set()
        self.edgeset = {}
        self.edgefullset={}
        self.edgenode = {}
        self.node_id_set = set()
        self.nodeset = {}

    def add_edge(self, edge):
        self.edge_id_set.add(edge.id)
        self.edgeset[edge.id] = edge
        self.edgefullset[(edge.pointer.id,edge.pointee.id)] = edge
        self.edgenode[(edge.pointer.id, edge.pointee.id)] = edge.id
        if edge.pointer.id not in self.node_id_set:
            node = vertex_a(edge.pointer)
            node.heads.append(edge)
            self.nodeset[edge.pointer.id] = node
            self.node_id_set.add(edge.pointer.id)
        else: 
            self.nodeset[edge.pointer.id].heads.append(edge)
        if edge.pointee.id not in self.node_id_set:
            node = vertex_a(edge.pointee)
            node.tails.append(edge)
            self.nodeset[edge.pointee.id] = node
            self.node_id_set.add(edge.pointee.id)
        else:
            self.nodeset[edge.pointee.id].tails.append(edge)

    def init_cost1(self,_label_lane):
        volume1 = {}
        for l in self.edge_id_set:
            volume1[l] = 0
        volume2 = {}
        for l in self.edge_id_set:
            volume2[l] = 0
        self.update_cost1(volume1,volume2,_label_lane)
    
    def update_cost1(self,volume1,volume2,_label_lane):
        for l in self.edgeset.keys():
            for j in range(0,6):
                if l in ["E{:0>3}".format(j)]:
                    self.edgeset[l].cal_weight1(volume1[l],volume2[l],_label_lane[j])
                    continue
class edge_b:
    def __init__(self, edge_info):
        self.id = edge_info[0]
        self.pointer = vertex_b(edge_info[1])
        self.pointee = vertex_b(edge_info[2])
        self.fft = float(edge_info[3])  # fre flow travel time
        self.capacity2 = float(edge_info[4])
        self.alpha = float(edge_info[5])
        self.beta = float(edge_info[6])
        self.cost = float('inf')
        self.volume1 = 0 # flow
        self.volume2 = 0
        self.capacity1=float(edge_info[7].strip())
        
    # calculate the weight by BPR function:
    def cal_weight2(self,volume1, volume2,_label_lane):
        """
            BPR_function
        """
        if _label_lane==1:
            self.cost = self.fft*(1+self.alpha*np.power(volume2/self.capacity2, self.beta))
        else:
            self.cost = self.fft*(1+self.alpha*np.power((volume1+volume2)/(self.capacity1+self.capacity2),self.beta))
        return self.cost

    def __eq__(self, other):
        """
            compare two edges are equal or not 
            not clear where to use
        """
        if isinstance(other, self.__class__):
            return (self.pointer.id == other.pointer.id) and (self.pointee.id == other.pointee.id)
        else:
            return False


class vertex_b:
    def __init__(self, node_id):
        self.id = node_id
        self.tails = []
        self.heads = []
        self.prev = None
        self.potential = float('inf')

    def __cmp__(self, other):
        """
            compare the label of two links 
            used in the shortest path
        """
        return __cmp__(self.potential, other.potential)


class network_b:
    """
        use "set" data type, which can not be assessed by index
    """
    def __init__(self, netname):
        self.name = netname
        self.edge_id_set = set()
        self.edgeset = {}
        self.edgefullset={}
        self.edgenode = {}
        self.node_id_set = set()
        self.nodeset = {}

    def add_edge(self, edge):
        self.edge_id_set.add(edge.id)
        self.edgeset[edge.id] = edge
        self.edgefullset[(edge.pointer.id,edge.pointee.id)] = edge
        self.edgenode[(edge.pointer.id, edge.pointee.id)] = edge.id
        if edge.pointer.id not in self.node_id_set:
            node = vertex_b(edge.pointer)
            node.heads.append(edge)
            self.nodeset[edge.pointer.id] = node
            self.node_id_set.add(edge.pointer.id)
        else: 
            self.nodeset[edge.pointer.id].heads.append(edge)
        if edge.pointee.id not in self.node_id_set:
            node = vertex_b(edge.pointee)
            node.tails.append(edge)
            self.nodeset[edge.pointee.id] = node
            self.node_id_set.add(edge.pointee.id)
        else:
            self.nodeset[edge.pointee.id].tails.append(edge)

    def init_cost2(self,_label_lane):
        volume2 = {}
        for l in self.edge_id_set:
            volume2[l] = 0
        volume1 = {}
        for l in self.edge_id_set:
            volume1[l] = 0
        self.update_cost2(volume1,volume2,_label_lane)

    def update_cost2(self,volume1,volume2,_label_lane):
        for l in self.edgeset.keys():
            for j in range(0,6):
                if l in ["E{:0>3}".format(j)]:
                    self.edgeset[l].cal_weight2(volume1[l],volume2[l],_label_lane[j])
                    continue
