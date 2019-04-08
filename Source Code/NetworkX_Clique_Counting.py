import snap
import time
import networkx as nx
from networkx.algorithms.clique import find_cliques

fileName = "usairport.txt"

G = nx.read_edgelist(fileName, delimiter=" ", create_using=nx.Graph(), nodetype=int)

tStart = time.time()

cliques = list(find_cliques(G))

tEnd = time.time()

count = 0

k = 4

for c in cliques:
    if len(c) == k:
        count = count + 1
        
print count

print "Time: ", tEnd - tStart
