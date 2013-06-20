import random
import pickle
import numpy as np

random.seed(2)

def gen_data(G):
    edgeProb = np.array([
        [0.8, 0.7, 0.3, 0.7],
        [0.2, 0.8, 0.7, 0.2],
        [0.3, 0.2, 0.8, 0.7],
        [0.2, 0.8, 0.2, 0.7],
        ])
    clstrSz = np.array([
        [90, 150, 100, 100],
        [150, 110, 50, 90],
        ]).astype(np.int)

    N_GROUP = edgeProb.shape[0]
    noise = 0

    x, y = 0, 0
    for ig in range(clstrSz[0, :].size):
        for i in range(clstrSz[0, ig]):
            G.add_node('u-'+str(x), 0)
            y = 0
            for jg in range(clstrSz[1, :].size):
                for j in range(clstrSz[1, jg]):
                    G.add_node('i-'+str(y), 1)
                    if random.uniform(0, 1) < edgeProb[ig, jg]:
                        G.add_edge_by_name('u-'+str(x), 'i-'+str(y))
                        if edgeProb[ig, jg] < 0.5: noise += 1
                    elif edgeProb[ig, jg] > 0.5: noise += 1
                    y += 1
            x += 1
                        
    print 'Noise Amount:', noise

    pickle.dump(((G.V, G.A), (G.V, None)), \
        open('bipartite_orig', 'w'))
    return G
