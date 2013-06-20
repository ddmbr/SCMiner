SCMiner(KDD '12)
=================

PROJECT HOME: https://github.com/ddmbr/SCMiner

Overview
--------

This is a working implementation of the SCMiner proposed on KDD '12 by Feng et al. It's written in Python, with NumPy and binary operation optimized. Some of the algorithm is modified to improve both its effectiveness and efficiency. Those who are interested may check for details in the technical report.

Here's some useful information about what's included:

+ doc/report.pdf(The technical report)
+ doc/pre.html(Presentation note in HTML5 format)
+ src/runtest.py(Use this to run the code)
+ src/gen\_img.py(Visualize the state of bipartite and save it as an image)
+ src/gen\_grid.py(Visualize the state of bipartite **on the fly**)

Usage
-----

Use runtest.py to run a test case. It may recieve one parameter, the epsilon, for example,

    python runtest.py 0.15

If no parameter is passed, the default value will be 0.1.

To visualize the node clustering process, either run the following:

    python gen_grid.py bipartite_half

in juxtaposed with runtest.py, or use:

    python gen_img.py bipartite output.png

to generate a final result afterwards.

Here 'bipartite\_half' and 'bipartite' are simply cPickle files for saving bipartites.

There're various test cases available. To try each of them, first open up the file runtest.py. With the directions in the code another new test can be performed just by uncommenting a line.

Swicthes
-----------------

There're some 'switches' available in the code for the algorithm. For example MOD\_COST in SCMiner.py and LAZY\_HOP2SIM in Bipartite.py. These correspond to some modifications to the original algorithm, introduced and explained in the report. Switching them on and off will lead to some differences in the result.

