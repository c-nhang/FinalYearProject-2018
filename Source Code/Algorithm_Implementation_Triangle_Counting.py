import snap
import time

# G = Graph, M = threshold
def algorithm(G, M):
    #Pruning Step
    P = 1
    Count = 0
    while P == 1:
        P = 0
        for node in G.Nodes():
            nodeID = node.GetId()
            degree = node.GetDeg()
            if degree <= M or degree > G.GetNodes() - 2:
                if degree <= M and degree > 1:
                    for i in range(degree - 1):
                        for j in range(i + 1, degree):
                            a = node.GetNbrNId(i)
                            b = node.GetNbrNId(j)
                            if G.IsEdge(a, b):
                                Count = Count + 1
                if degree > M and degree > G.GetNodes()-2:
                    Count = Count + G.GetEdges() - node.GetDeg()
                P = 1
                G.DelNode(nodeID)

    #Hierarchical Clustering Step
    if G.GetNodes() > 5:
        H = snap.ConvertGraph(type(G), G)
        S = []
        i = 0    
        while H.GetNodes() > 0:
            S.append([])
            # randomly chosen a node with maximum degree
            S[i].append(snap.GetMxDegNId(H))
            j = 1
            HC = True
            
            while HC:
                # create an empty vector of integers
                s = snap.TIntV()
                # (Graph, StartNId, Hop: distance, NIdV: store nodes, IsDir: directed?)
                snap.GetNodesAtHop(H, S[i][0], j, s, True)
                if len(s) != 0:
                    S[i].append(s)
                    j = j + 1
                else:
                    HC = False
                    
            H.DelNode(S[i][0])
            for j in range(1, len(S[i])):
                for nodeID in S[i][j]:
                    H.DelNode(nodeID)
            i = i + 1
            
        subgraphs = [[] for x in range(len(S))]
        
        #Counting Step
        for i in range(len(S)):
            for j in range(1, len(S[i])):
                G01 = snap.ConvertSubGraph(snap.PUNGraph, G, S[i][j])
                subgraphs[i].append(G01)
            Count = Count + subgraphs[i][0].GetEdges()
            G.DelNode(S[i][0])
            
        for i in range(len(S)):
            for j in range(1, len(S[i])):
                
                for nodeID in S[i][j]:
                    U = []
                    M = []
                    for t in range(G.GetNI(nodeID).GetDeg()):
                        a = G.GetNI(nodeID).GetNbrNId(t)
                        #check lower level
                        if j < len(S[i]) - 1:
                            if subgraphs[i][j].IsNode(a):
                                U.append(a)
                        #check upper level
                        if j > 1:        
                            if subgraphs[i][j - 2].IsNode(a):
                                M.append(a)
                                
                    for s in range(len(U)):
                        for t in range(s + 1, len(U)):
                            if subgraphs[i][j].IsEdge(U[s], U[t]):
                                Count = Count + 1
                                
                    for s in range(len(M)):
                        for t in range(s + 1,len(M)):
                            if subgraphs[i][j - 2].IsEdge(M[s], M[t]):
                                Count = Count + 1
                                
        for i in range(len(S)):
            for j in range(len(S[i]) - 1):
                Count = Count + algorithm(subgraphs[i][j], M)
                
    return Count

#Threshold M
for M in range(0,15):
    #Graph G
    G = snap.LoadEdgeList(snap.PUNGraph, "facebook_combined1.txt", 0, 1)
    for node in G.Nodes():
        nodeID = node.GetId()
        #remove self-loops
        if G.IsEdge(nodeID, nodeID):
            G.DelEdge(nodeID, nodeID)
            
    tStart = time.time()
    Count = algorithm(G, M)
    print "Triangles: ", Count
    
    tEnd = time.time()
    print "Time: ", tEnd - tStart