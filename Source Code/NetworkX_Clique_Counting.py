import snap
import time

import networkx as nx

fileName = "usairport.txt"
G = nx.read_edgelist(fileName, delimiter=" ", create_using=nx.Graph(), nodetype=int)
print(type(G), G)
from networkx.algorithms.clique import find_cliques
tStart = time.time()
cliques = list(find_cliques(G))
tEnd = time.time()
count = 0

for c in cliques:
    if len(c) == 4:
        count = count + 1
        print c
        
print count

print "Time: ", tEnd - tStart