"""
Note: Sizes of groups are pre-computed
"""
import os
import copy
import math
import numpy as np
# import numpypy as np
# import pygraphviz as pgv
# import pylab

DTYPE = np.int
# DTYPE = int
LAZY_HOP2SIM = False

class Bipartite:
    """
    This is the Bipartite class accelerated by NumPy
    """
    def __init__(self, V=None, E=None):
        if V == None and E == None:
            self.parts = [{}, {}]
            self.A = np.array([]).reshape((0, 0)).astype(DTYPE)
            self.ginfo = [np.array([]), np.array([])]

            # self.group = [{}, {}]
            self.attrs = [{}, {}]

            self.V = (self.parts, self.ginfo, self.attrs)
            self.E = self.A
        elif V != None and E == None:
            self.V = (self.parts, self.ginfo, self.attrs) = \
                copy.deepcopy(V)
            self.E = self.A = np.zeros((len(self.parts[0]), \
                len(self.parts[1]))).astype(DTYPE)
        elif V != None and E != None:
            self.V = (self.parts, self.ginfo, self.attrs) = \
                copy.deepcopy(V)
            self.E = A = copy.deepcopy(E)
            
        self._hop2sim = [np.array([]).reshape((0, 0)), \
            np.array([]).reshape((0, 0))]

    def prepare(self, with_hop2sim=True):
        self.setSize = [np.ones(self.A.shape[0]), \
            np.ones(self.A.shape[1])]
        for p in [0, 1]:
            self.ginfo[p] = \
                np.zeros((self.A.shape[p], \
                    self.A.shape[p])).astype(DTYPE)
            np.fill_diagonal(self.ginfo[p], 1)

        if with_hop2sim:
            if LAZY_HOP2SIM:
                self._hop2sim[0].fill(-1)
                self._hop2sim[1].fill(-1)
            else:
                self.cal_all_hop2sim()
        assert self.A.dtype == np.int

    def add_node(self, name, part):
        """
        Add a node without any edge connecting to it.
        If the name already exist, the node won't be
        created.
        Index for the newly created node will be returned.

        @name: Name of the node to be created.
        @part: Part to join, should be 0 or 1
        """
        if name not in self.parts[part]:
            self.parts[part][name] = self.A.shape[part]
            if part == 0:
                extra = np.zeros((1, self.A.shape[1]))
            elif part == 1:
                extra = np.zeros((self.A.shape[0], 1))

            # Matrix
            self.A = np.concatenate((self.A, extra.astype(DTYPE)), \
                axis=part)

            # Hop2Sim
            self._hop2sim[part] = \
                np.resize(self._hop2sim[part], \
                    (self._hop2sim[part].shape[0]+1, \
                    self._hop2sim[part].shape[1]+1))

            # Index & name
            idx = self.parts[part][name]

            # Group info
            # self.group[part][idx] = {idx,}

            # Attrs
            self.attrs[part][self.parts[part][name]] = {}

        return self.parts[part][name]

    def set_attrs(self, name, part, attr, value):
        self.attrs[part][self.parts[part][name]][attr] = value

    def add_edge_by_name(self, name0, name1):
        """
        Add an edge, providing two corresponding
        nodes' names. If names doesn't exist, new nodes
        will be created accordingly.

        Notice that the node named 'name0' will be in
        part 0, and the 'name1' node in part 1.

        @name0: One node.
        @name1: Another node.
        """

        assert isinstance(name0, str)
        assert isinstance(name1, str)

        idx0 = self.add_node(name0, 0)
        idx1 = self.add_node(name1, 1)

        self.add_edge(idx0, idx1)

    def add_edge(self, idx0, idx1):
        """
        Add an edge providing two actual nodes.
        """
        assert idx0 != None and idx1 != None
        self.A[idx0, idx1] = 1

    def merge_nodes(self, nodes=None, part=None):
        """
        @nodes: iteratable object
        @part:
        """
        nodes = list(nodes)
        ginfo = self.ginfo[part]

        # Modify group info
        for other in nodes[1:]:
            ginfo[nodes[0], :] |= ginfo[other]
            ginfo[other, :].fill(0)
            self.setSize[part][nodes[0]] += \
                self.setSize[part][other]
            self.setSize[part][other] = 0

        # inform his friends
        # if part == 0:
        #     for i in self.A[nodes[0], :]:
        #         self.A[:, i] |= ginfo[nodes[0], :]
        # elif part == 1:
        #     for i in self.A[:, nodes[0]]:
        #         self.A[i, :] |= ginfo[nodes[0], :]

        # delete nodes
        if part == 0: self.A[nodes[1:], :] = 0
        elif part == 1: self.A[:, nodes[1:]] = 0

    def super_nodes(self, part):
        res = np.nonzero(self.ginfo[part].max(axis=1))[0]
        return res

    def remove_edge_by_name(self, name0, name1):
        idx0 = self.parts[0][name0]
        idx1 = self.parts[1][name0]
        self.remove_edge(idx0, idx1)

    def remove_edge(self, idx0, idx1):
        self.A[idx0, idx1] = 0

    def invert_edge(self, idx0s, idx1s):
        # print idx0, idx1
        try:
            for idx0 in idx0s:
                self.A[idx0, :][:, idx1s] ^= 1
        except:
            self.A[idx0s, idx1s] ^= 1

    def neighbors(self, idx, part, bitmap=True):
        """
        Return a set of neighbors of a given node.
        """
        if part == 0:
            res = self.A[idx, :]
        elif part == 1:
            res = self.A[:, idx]
        if bitmap == False:
            res = res.nonzero()[0]
        return res

    def hop2sim(self, idx0, idx1, part):
        if idx0 < idx1: idx0, idx1 = idx1, idx0

        if LAZY_HOP2SIM and self._hop2sim[part][idx0, idx1] < 0:
            self.cal_hop2sim(idx0, idx1, part)
        return self._hop2sim[part][idx0, idx1]

    def cal_hop2sim(self, sidx0, sidx1, part):
        if sidx0 < sidx1: sidx0, sidx1 = sidx1, sidx0

        commonNeighbors = self.neighbors(sidx0, part) & \
            self.neighbors(sidx1, part)
        allNeighbors = self.neighbors(sidx0, part) | \
            self.neighbors(sidx1, part)
        # commonNeighbors = self.ginfo[part][commonNeighbors.nonzero()[0], :].max(axis=0).nonzero()[0]
        # allNeighbors = self.ginfo[part][allNeighbors.nonzero()[0], :].max(axis=0).nonzero()[0]

        # # print commonNeighbors
        # assert np.array_equal(commonNeighbors, np.unique(commonNeighbors))
        # assert np.array_equal(allNeighbors, np.unique(allNeighbors))

        # commonNeighbors = np.count_nonzero(commonNeighbors)
        # allNeighbors = np.count_nonzero(allNeighbors)

        t = commonNeighbors.nonzero()[0]
        commonNeighbors = np.sum(self.setSize[part^1][t])
        t = allNeighbors.nonzero()[0]
        allNeighbors = np.sum(self.setSize[part^1][t])

        if allNeighbors == 0:
            self._hop2sim[part][sidx0, sidx1] = 0
        else:
            self._hop2sim[part][sidx0, sidx1] = \
                commonNeighbors*1./allNeighbors

        # if not LAZY_HOP2SIM:
        #     for idx0 in self.group[part][sidx0]:
        #         for idx1 in self.group[part][sidx1]:
        #             if idx0 < idx1: 
        #                 self._hop2sim[part][idx1, idx0] = \
        #                     self._hop2sim[part][sidx0, sidx1]
        #             else:
        #                 self._hop2sim[part][idx0, idx1] = \
        #                     self._hop2sim[part][sidx0, sidx1]
                    # self._hop2sim[part][idx1, idx0] = \
                    #     self._hop2sim[part][sidx0, sidx1]

    def update_hop2sim(self, idx0, part):
        # TODO
        S = self.super_nodes(part)

        # We only update super nodes
        if idx0 not in S: return

        for idx1 in S:
            if LAZY_HOP2SIM:
                self._hop2sim[part][idx0, idx1] = -1
                self._hop2sim[part][idx1, idx0] = -1
            else:
                self.cal_hop2sim(idx0, idx1, part)

    def cal_all_hop2sim(self, idx0=None, idx1=None, part=None):
        for part in [0, 1]:
            for idx0 in range(0, self.A.shape[part]):
                for idx1 in range(idx0, self.A.shape[part]):
                    self.cal_hop2sim(idx0, idx1, part)

    def set_size(self, S, part):
        S = list(S)
        return np.count_nonzero(self.ginfo[part][S, :])
        # return np.sum(self.ginfo[part][S, :])

    # def extend(self, S, part):
    #     extendS = set()
    #     for sidx in S:
    #         for idx in self.group[part][sidx]:
    #             extendS.add(idx)
    #     return extendS

    def coding_cost(self):
        V0 = np.nonzero(self.ginfo[0].max(axis=1))[0]
        V1 = np.nonzero(self.ginfo[1].max(axis=1))[0]

        n_edges = np.count_nonzero(self.A[V0, :][:, V1])
        V0, V1 = V0.size, V1.size
        # print 'n_edges:', n_edges, 'V0:', V0, 'V1:', V1
        if n_edges == 0: return 0

        Pn = n_edges*1./(V0*V1)
        Pr = 1 - Pn
        # print 'Pn:', Pn, 'Pr:', Pr
        if Pn == 0: Hn = 0
        else: Hn = Pn*math.log(Pn, 2)
        if Pr == 0: Hr = 0
        else: Hr = Pr*math.log(Pr, 2)
        Ha = -(Hn+Hr)
        return Ha*V0*V1

    def group_info_coding_cost(self, part=None):
        if part == None:
            return self.group_info_coding_cost(0) + \
                self.group_info_coding_cost(1)

        ginfo = self.ginfo[part]
        mnum = ginfo.sum(axis=1)
        gprob = mnum*1. / ginfo.shape[0]
        cost = 0
        for prob, num in zip(gprob, mnum):
            if prob != 0:
                cost += np.log2(1/prob)*num
        return cost

    def has_edge(self, idx0, idx1):
        if self.A[idx0, idx1] == 1:
            return True
        else: return False

    def gen_graph(self, fn='graph', opt='super'):
        graph = pgv.AGraph(strict=False, compound=True)
        #graph.layout()

        inverted_dict = self.ufset.inverted_dict()
        fathers = [[father for father in self.parts[i] if father in inverted_dict] for i in [0, 1]]
        for part in [0, 1]:
            pos_y = 0
            for father in fathers[part]:
                bunch = []
                for node in inverted_dict[father]:
                    name = node.name.decode('UTF-8')

                    graph.add_node(name)
                    bunch += [name]
                    n = graph.get_node(name)
                    n.attr['pos'] = "%f,%f"%(100+300*part, 100+pos_y*100)
                    n.attr['color'] = ['blue', 'black'][part]
                    pos_y += 1
                if opt == 'super':
                    subgraph = graph.add_subgraph(nbunch=bunch, name='cluster_'+father.name.decode('UTF-8'))

        if opt == 'super':
            pass
            for node in fathers[0]:
                for dest_node in self.edges[node]:
                    if dest_node not in inverted_dict: continue
                    graph.add_edge(node.name.decode('UTF-8'), dest_node.name.decode('UTF-8'))
                    e = graph.get_edge(node.name.decode('UTF-8'), dest_node.name.decode('UTF-8'))
                    e.attr['lhead'] = 'cluster_'+node.name.decode('UTF-8')
                    e.attr['ltail'] = 'cluster_'+dest_node.name.decode('UTF-8')
        else:
            for node in self.parts[0]:
                for dest_node in self.edges[node]:
                    graph.add_edge(node.name.decode('UTF-8'), dest_node.name.decode('UTF-8'))

        print graph.string()
        graph.write(fn+'.dot')
        os.system('sh make_graph.sh '+fn+'.dot')
        os.system('feh -ZF '+fn+'.png')
        # graph.draw(fn+'.png', prog='fdp', args='-n2')

        # im = pylab.imread(fn+'.png')
        # pylab.imshow(im)
        # pylab.show()

if __name__ == '__main__':
    G = Bipartite()
    G.add_edge_by_name('china', 'js')
    G.add_edge_by_name('taiwan', 'js')
    G.add_edge_by_name('xxx', 'html')
    # G.add_edge_by_name('taiwan', 'php')
    G.add_edge_by_name('singapore', 'html')
    G.add_node('php', 1)
    G.prepare()

    china = G.parts[0]['china']
    taiwan = G.parts[0]['taiwan']
    xxx = G.parts[0]['xxx']
    singapore = G.parts[0]['singapore']

    print G.hop2sim(china, taiwan, 0)
    G.merge_nodes([taiwan, china], 0)
    G.merge_nodes([xxx, singapore], 0)
    print G.ginfo[0][(taiwan, xxx), :].max(axis=0)
