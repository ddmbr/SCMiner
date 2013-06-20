import copy
import cPickle
import time
import random
import numpy as np
# import numpypy as np
import pylab
pylab = []

# from reconstruct        import validate
from Bipartite          import Bipartite
from mdllogger          import logmdl
from mdllogger          import savemdl

RANDOMIZED_EXPAND = False
MOD_COST = False
SHOW_GRAPH = False
WITH_GCC = True
picNum = 0

if SHOW_GRAPH:
    pylab.ion()
    f = pylab.figure()
    ax0 = f.add_subplot(121)
    ax1 = f.add_subplot(122)

class SCMiner:
    def __init__(self, G, eps=0.05):
        """
        Initialize a SCMiner.
        @G: The bipartite graph to summarize
        @eps: The reduce step
        """
        # Initialize Summary Graph and Addition Graph
        self.Gs = G
        # self.Ga = Bipartite()
        self.Ga = Bipartite(V=G.V)

        self.eps = eps

        # prepare hop2sim
        self.Gs.prepare()
        self.Ga.prepare(with_hop2sim=False)

        # Compute mincc
        self.mincc = self.coding_cost()
        print 'Initial CC:', self.mincc

        # Result will be stored here
        self.best = \
            cPickle.dumps(
                ((self.Gs.V, self.Gs.A),\
                (self.Ga.V, self.Ga.A)),
                -1)
        cPickle.dump(((self.Gs.V, self.Gs.A), \
            (self.Ga.V, self.Ga.A)), \
            open('bipartite_half', 'w'))

    def summarize(self):
        global picNum
        # Initialize the threshold
        MAX_TH = 1
        th = MAX_TH

        Gs, Ga = self.Gs, self.Ga
        start_t = time.clock()

        while th > 0:
            print '... th=%f, Calculating...' % th

            allGroup = [[], []]
            for part in [0, 1]:
                # Get super nodes
                U = set(Gs.super_nodes(part))
                # print 'super nodes of part %d'%part, len(U)
                while len(U) != 0:
                    group = []
                    for node in U:
                        if group == []:
                            group += [node]
                            continue

                        if RANDOMIZED_EXPAND:
                            other = random.choice(group)
                            if Gs.hop2sim(other, \
                                node, part) > th:
                                group += [node]
                        else:
                            if Gs.hop2sim(group[0], \
                                node, part) > th:
                                group += [node]

                    assert group != []
                    for node in group: U.remove(node)
                    group = set(group)
                    if len(group)>1:
                        allGroup[part] += [group]
                        # break

            nodesToUpdate = [set(), set()]
            for part in [0, 1]:
                for group in allGroup[part]:
                    print 'Merge nodes of part %d:'%part, group
                    # try:
                    self.modify_edge(group, part, \
                        nodesToUpdate[part])
                    Gs.merge_nodes(group, part)
                    # except: break

                    # compute cc
                    ccGs = self.Gs.coding_cost()
                    ccGa = self.Ga.coding_cost()
                    ccGroup = self.Gs.group_info_coding_cost()
                    print '    CC Gs:', ccGs, \
                        'CC Ga:', ccGa,
                    if WITH_GCC:
                        print 'CC Group:', ccGroup
                        cc = ccGs + ccGa + ccGroup
                    else:
                        print ''
                        cc = ccGs + ccGa
                    print '    CC:', cc, 'MinCC:', self.mincc
                    logmdl([cc, group, part])
                    if cc < self.mincc:
                        print '... Save current best!'
                        self.best = \
                            cPickle.dumps(
                                ((self.Gs.V, self.Gs.A),\
                                (self.Ga.V, self.Ga.A)),
                                -1)
                        cPickle.dump(((self.Gs.V, self.Gs.A), \
                            (self.Ga.V, Ga.A)), \
                            open('bipartite_half', 'w'))

                        self.mincc = cc

            for part in [0, 1]:
                # Update hop2sim
                for idx in nodesToUpdate[part]:
                    self.Gs.update_hop2sim(idx, part^1)
            # PyLab
            if SHOW_GRAPH:
                ax0.imshow(self.Gs._hop2sim[0][self.Gs.super_nodes(0), :][:, self.Gs.super_nodes(0)], \
                    cmap=pylab.cm.gray)
                ax1.imshow(self.Gs._hop2sim[1][self.Gs.super_nodes(1), :][:, self.Gs.super_nodes(1)], \
                    cmap=pylab.cm.gray)
                picNum += 1
                # pylab.imsave(fname="log/pic-"+str(picNum)+".png", \
                # pylab.savefig(fname="log/pic-"+str(picNum)+".png", \
                #     bbox_inches='tight')
                pylab.draw()


            if allGroup == [[], []]:
                th -= self.eps
            else:
                th = MAX_TH

        end_t = time.clock()
        print '... Finished. %d s elapsed'%(end_t-start_t)

        # PyLab
        # pylab.ioff()
        # pylab.imshow(self.Gs._hop2sim[0], cmap=pylab.cm.gray)
        # pylab.show()

        # MDL Debug
        savemdl()
        cPickle.dump(self.mincc, open("mincc", "w"))
        return cPickle.loads(self.best)

    def modify_edge(self, group, part, nodesToUpdate=set()):
        """
        Modify edges in a group to unify their connections.
        """
        group = list(group)
        bgroup = np.zeros(self.Gs.A.shape[part]).astype(int)
        bgroup[group] = 1

        allNeighbors = self.Gs.neighbors(group[0], part)
        commonNeighbors = self.Gs.neighbors(group[0], part)

        # Calculate allNeighbors and commonNeighbors
        for idx in group:
            allNeighbors = allNeighbors | \
                self.Gs.neighbors(idx, part)
            commonNeighbors = commonNeighbors & \
                self.Gs.neighbors(idx, part)

        # print 'all'
        # print allNeighbors
        # print 'common'
        # print commonNeighbors

        # Modify edges of the group to make their links same
        nodesToResolved = allNeighbors - commonNeighbors
        # print 'resolve'
        # print nodesToResolved
        nodesToResolved = nodesToResolved.nonzero()[0]

        for idx in nodesToResolved:
            # Desicide whether to link or unlink,
            # to a specific node(idx)
            removeSet = bgroup & \
                self.Gs.neighbors(idx, part^1)
            addSet = bgroup - removeSet

            removeSet = removeSet.nonzero()[0]
            addSet = addSet.nonzero()[0]

            if not MOD_COST:
                pass
                costRemove = np.sum(self.Gs.setSize[part][removeSet])
                costAdd = np.sum(self.Gs.setSize[part][addSet])
            else:
                # My hack
                a = self.Gs.ginfo[part][removeSet, :].max(axis=0).nonzero()[0]
                b = self.Gs.ginfo[part^1][idx, :].nonzero()[0]
                if part == 0:
                    costRemove = \
                        a.size * b.size - \
                            2 * np.count_nonzero(self.Ga.A[a, :][:, b])
                elif part == 1:
                    costRemove = \
                        a.size * b.size - \
                            2 * np.count_nonzero(self.Ga.A[b, :][:, a])

                a = self.Gs.ginfo[part][addSet, :].max(axis=0).nonzero()[0]
                b = self.Gs.ginfo[part^1][idx, :].nonzero()[0]
                if part == 0:
                    costAdd = \
                        a.size * b.size - \
                            2 * np.count_nonzero(self.Ga.A[a, :][:, b])
                elif part == 1:
                    costAdd = \
                        a.size * b.size - \
                            2 * np.count_nonzero(self.Ga.A[b, :][:, a])

            # print costRemove, costAdd
            # Decide to remove or add
            if costRemove < costAdd:
                modifySet = removeSet
            elif costAdd <= costRemove:
                modifySet = addSet
            # elif costRemove == costAdd:
            #     try: pick = random.choice(commonNeighbors)
            #     except:
            #         # no common neighbors
            #         # reason is unclear
            #         print '... WARN: No common neighbors!'
            #         raise Exception
            #     if self.Gs.hop2sim(pick, idx, part^1) > 0.5:
            #         modifySet = addSet
            #     else: modifySet = removeSet

            a = self.Gs.ginfo[part][modifySet, :].max(axis=0).nonzero()[0]
            b = self.Gs.ginfo[part^1][idx, :].nonzero()[0]
            # print 'a', a
            # print 'b', b
            # print 'modifySet', modifySet
            # print 'idx', idx
            if part == 0:
                # print self.Gs.A[modifySet, :][:, idx]
                self.Gs.invert_edge(modifySet, idx)
                # print self.Gs.A[modifySet, :][:, idx]
                self.Ga.invert_edge(a, b)
                # validate(self.Gs.V, self.Gs.A, self.Ga.V, self.Ga.A)
            elif part == 1:
                self.Gs.invert_edge(idx, modifySet)
                self.Ga.invert_edge(b, a)

        for idx in nodesToResolved: nodesToUpdate.add(idx)

    def coding_cost(self):
        res = self.Gs.coding_cost() + \
            self.Ga.coding_cost()
        if WITH_GCC:
            return res + self.Gs.group_info_coding_cost()
        else: return res
