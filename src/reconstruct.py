import sys
import cPickle
import pickle
# from Bipartite import Bipartite
# from Bipartite import SuperNode
from Bipartite import Bipartite
import pygame
import numpy as np

def reconstruct(Gs_V, Gs_E, Ga_V, Ga_E, output=None):
    As = Gs_E
    Aa = Ga_E
    A = np.zeros(Aa.shape).astype(np.int)
    ginfo = Gs_V[1]
    for i in range(Aa.shape[0]):
        for j in range(Aa.shape[1]):
            # assert ginfo[0][:, i].nonzero()[0].shape[0] == 1
            # assert ginfo[1][:, i].nonzero()[0].shape[0] == 1
            A[i, j] = As[ginfo[0][:, i].nonzero()[0], ginfo[1][:, j].nonzero()[0]]^Aa[i, j]

    if output != None:
        pickle.dump(((Gs_V, A), (None, None)), open(output, "w"))
    return A

(d0, E_orig), (d1, d2) = pickle.load(open("bipartite_orig"))
def validate(Gs_V, Gs_E, Ga_V, Ga_E):
    A = reconstruct(Gs_V, Gs_E, Ga_V, Ga_E)

    # print np.where(E_orig != A)
    print A
    print E_orig
    assert np.array_equal(E_orig, A)

if __name__ == '__main__':
    assert len(sys.argv) > 2
    (Gs_V, Gs_E), (Ga_V, Ga_E) = \
        pickle.load(open(sys.argv[-1]))
    E_ = reconstruct(Gs_V, Gs_E, Ga_V, Ga_E, output="avatar")

    (Gs_V, Gs_E), (Ga_V, Ga_E) = \
        pickle.load(open(sys.argv[-2]))

    print Gs_E
    print E_
    assert np.array_equal(Gs_E, E_)
