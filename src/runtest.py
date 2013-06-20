import test.newsgroups.test         as newsgroupsTest
import test.toy_two_person.test     as twoPersonTest
import test.toy_three_person.test   as threePersonTest
import test.toy_noise.test          as noiseTest
import test.movielens.test          as movielensTest
import test.synthetic_bp1.test      as syntheticTest1
import test.synthetic_bp2.test      as syntheticTest2
import test.synthetic_bp3.test      as syntheticTest3
import test.synthetic_bp4.test      as syntheticTest4
import test.synthetic_bp5.test      as syntheticTest5
import test.synthetic_bp6.test      as syntheticTest6
# import test.delicious.test          as delicious

from SCMiner        import SCMiner
from Bipartite      import Bipartite
# import utils
import pickle
import sys

eps = 0.1
if len(sys.argv) > 1:
    eps = float(sys.argv[-1])

G = Bipartite()
# G = newsgroupsTest.gen_data(G)
# G = twoPersonTest.gen_data(G)
# G = threePersonTest.gen_data(G)
# G = noiseTest.gen_data(G)
# G = movielensTest.gen_data(G)
# G = syntheticTest1.gen_data(G)
# G = syntheticTest2.gen_data(G)
G = syntheticTest3.gen_data(G)
# G = syntheticTest4.gen_data(G)
# G = syntheticTest5.gen_data(G)
# G = syntheticTest6.gen_data(G)
# G = delicious.gen_data(G)

miner = SCMiner(G, eps)
Gs_t, Ga_t = miner.summarize()
pickle.dump((Gs_t, Ga_t), open('bipartite', 'w'))
