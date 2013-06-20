import sys
import cPickle
from Bipartite      import Bipartite
# from Bipartite      import SuperNode
from reconstruct    import reconstruct
import pygame
import random

assert len(sys.argv) > 2
Gs_V, Gs_E, Ga_V, Ga_E, A = None, None, None, None, None
groups = [[], []]
gr = [[], []]
colors = {}
# Read bipartite
def read_bipartite():
    global Gs_V, Gs_E, Ga_V, Ga_E, A
    global gr, groups, colors
    succ = False
    while not succ:
        try:
            (Gs_V, Gs_E), (Ga_V, Ga_E) = cPickle.load(open(sys.argv[-2]))
            succ = True
        except: pass
    if Ga_E != None:
        A = reconstruct(Gs_V, Gs_E, Ga_V, Ga_E)
        ginfo = Gs_V[1]
        print ginfo
        for p in [0, 1]:
            # groups[p] = sorted([(g, i) for i, g in enumerate(ginfo[p])])
            for i in range(ginfo[p].shape[0]):
                for j in range(ginfo[p].shape[0]):
                    if ginfo[p][i, j] == 1:
                        groups[p].append((i, j))
            gr[p] = set([t[0] for t in groups[p]])
        for g0 in gr[0]:
            for g1 in gr[1]:
                if g0 not in colors: colors[g0] = {}
                if g1 not in colors[g0]:
                    colors[g0][g1] = (random.randint(0, 225), \
                        random.randint(0, 225), \
                        random.randint(0, 225))
    else: A = Gs_E
# read_bipartite()

GRID_SIZE = 2
START_X = 20
START_Y = 100
read_bipartite()
window = pygame.Surface((Gs_E.shape[1]*GRID_SIZE+START_X*2, \
    Gs_E.shape[0]*GRID_SIZE+START_Y*2))
window.fill((0xff, 0xff, 0xff))

if Ga_E != None:
    cur_g0 = -1
    cur_g1 = -1
    for t0 in range(len(groups[0])):
        for t1 in range(len(groups[1])):
            if A[groups[0][t0][1], groups[1][t1][1]] != 0:
            # if Gs_E[groups[0][t0][0], groups[1][t1][0]] != 0:
                pygame.draw.rect(window,
                    colors[groups[0][t0][0]][groups[1][t1][0]],
                    (START_X+t1*GRID_SIZE, START_Y+t0*GRID_SIZE,
                        GRID_SIZE, GRID_SIZE))
            if groups[1][t1][0] != cur_g1:
                cur_g1 = groups[1][t1][0]
                pygame.draw.line(window,
                    (150, 150, 150),
                    (START_X+t1*GRID_SIZE, START_Y),
                    (START_X+t1*GRID_SIZE, \
                        START_Y+A.shape[0]*GRID_SIZE))
        if groups[0][t0][0] != cur_g0:
            cur_g0 = groups[0][t0][0]
            pygame.draw.line(window,
                (150, 150, 150),
                (START_X, START_Y+t0*GRID_SIZE),
                (START_X+A.shape[1]*GRID_SIZE, \
                    START_Y+t0*GRID_SIZE))
else:
    for t0 in range(A.shape[0]):
        # color = (0, 0, 0)
        # if t0 in [3, 168]: color = (225, 0, 0)
        for t1 in range(A.shape[1]):
            color = (0, 0, 0)
            if t1 in [3, 168]:  color = (225, 0, 0)
            if A[t0, t1] != 0:
                pygame.draw.rect(window,
                    # colors[groups[0][t0][0]][groups[1][t1][0]],
                    color,
                    (START_X+t1*GRID_SIZE, START_Y+t0*GRID_SIZE,
                        GRID_SIZE, GRID_SIZE))

pygame.image.save(window, sys.argv[-1])
