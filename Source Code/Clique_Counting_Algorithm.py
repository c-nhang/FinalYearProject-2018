import snap
import time

def algorithm(G, threshold, clique_size):
    #Pruning Step
    P = 1
    T = 0
    a1 = []
    all_cliques = []
    while P == 1:
        P = 0 
        for NI in G.Nodes():
            NID = NI.GetId()
            d = NI.GetDeg()
            
            edgeList = {}
            if d <= threshold and d >= clique_size - 1:
                for i in range(d - 1):
                    for j in range(i + 1, d):
                        a = NI.GetNbrNId(i)
                        b = NI.GetNbrNId(j)
                        if G.IsEdge(a, b):
                            if a not in edgeList:
                                edgeList[a] = [b]
                            else:
                                edgeList[a].append(b)

                for node in edgeList:
                    neighbours = edgeList[node]
                    if len(neighbours) == 1:
                        cliqueList = [NID, node, neighbours[0]]
                        if len(cliqueList) >= clique_size:
                            all_cliques = ensureNoOverlap(all_cliques, cliqueList)
                    elif len(neighbours) > 1:
                        for i in range(len(neighbours)):
                            cliqueList = [NID, node, neighbours[i]]
                            for j in range(i + 1, len(neighbours)):
                                if G.IsEdge(neighbours[i], neighbours[j]):
                                		cliqueList.append(neighbours[j])
                            if len(cliqueList) >= clique_size:
                                all_cliques = ensureNoOverlap(all_cliques, cliqueList)
     
            if d <= threshold or d < clique_size - 1:
                P = 1
                G.DelNode(NID)
     
    for q in all_cliques:
        if len(q) == clique_size:
            print q, " Pruning"
            a1.append(q)
            T = T + 1
    for a in G.Nodes():
        print a.GetId(), a.GetDeg()
        
    #Hierarchical Clustering Step
    if G.GetNodes() >= clique_size:
        H = snap.ConvertGraph(type(G), G)
        S = []
        i = 0    
        while H.GetNodes() > 0:
            S.append([])
            # randomly chosen a node with maximum degree
            S[i].append(snap.GetMxDegNId(H))

            j = 1
            TTT = True
            while TTT:
                # create an empty vector of integers
                s = snap.TIntV()
                # (Graph, StartNId, Hop: distance, NIdV: store nodes, IsDir: directed?)
                snap.GetNodesAtHop(H, S[i][0], j, s, True)
                if len(s) != 0:
                    S[i].append(s)
                    j = j + 1
                else:
                    TTT = False

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
                
        for i in range(len(S)):
            C1 = snap.TIntV()
            C1.Add(S[i][0])
            for x in S[i][1]: 
                C1.Add(x)
            C01 = snap.ConvertSubGraph(snap.PUNGraph, G, C1)            
            all_cliques = []
            for NI in C01.Nodes():
                NID = NI.GetId()
                d = NI.GetDeg()           
                edgeList = {}
                for d1 in range(d - 1):
                    for d2 in range(d1 + 1, d):
                        a = NI.GetNbrNId(d1)
                        b = NI.GetNbrNId(d2)
                        if C01.IsEdge(a, b):
                            if a not in edgeList:
                                edgeList[a] = [b]
                            else:
                                edgeList[a].append(b)
                print edgeList
                for node in edgeList:
                    neighbours = edgeList[node]
                    if len(neighbours) == 1:
                        cliqueList = [NID, node, neighbours[0]]
                        if len(cliqueList) >= clique_size:
                            all_cliques = ensureNoOverlap(all_cliques, cliqueList)
                    elif len(neighbours) > 1:
                        for d1 in range(len(neighbours)):
                            cliqueList = [NID, node, neighbours[d1]]
                            for d2 in range(d1 + 1, len(neighbours)):
                                if G.IsEdge(neighbours[d1], neighbours[d2]):
                                		cliqueList.append(neighbours[d2])
                            if len(cliqueList) >= clique_size:
                                all_cliques = ensureNoOverlap(all_cliques, cliqueList)
            for q in all_cliques:
                if len(q) == clique_size:
                    print q, " C1"
                    a1.append(q)
                    T = T + 1         
            G.DelNode(S[i][0])
            
        for i in range(len(S)):
            for j in range(1, len(S[i])):
                for upnodeID in S[i][j]:
                    U = []
                    L = []
                    for t in range(G.GetNI(upnodeID).GetDeg()):
                        a = G.GetNI(upnodeID).GetNbrNId(t)
                        #check lower level
                        if j < len(S[i]) - 1:
                            if subgraphs[i][j].IsNode(a):
                                U.append(a)
                        #check upper level
                        if j > 1:        
                            if subgraphs[i][j - 2].IsNode(a):
                                L.append(a)
                                
                    edgeList = {}            
                    for s in range(len(U)):
                        for t in range(s + 1, len(U)):
                            if subgraphs[i][j].IsEdge(U[s], U[t]):
                                if U[s] not in edgeList:
                                    edgeList[U[s]] = [U[t]]
                                else:
                                    edgeList[U[s]].append(U[t])
                    edgeList2 = {}               
                    for s in range(len(L)):
                        for t in range(s + 1, len(L)):
                            if subgraphs[i][j - 2].IsEdge(L[s], L[t]):
                                if L[s] not in edgeList2:
                                    edgeList2[L[s]] = [L[t]]
                                else:
                                    edgeList2[L[s]].append(L[t])
                                        
                    all_cliques = []   
                    for node in edgeList:
                        neighbours = edgeList[node]
                        if len(neighbours) == 1:
                            cliqueList = [upnodeID, node, neighbours[0]]
                            if len(cliqueList) >= clique_size:
                                all_cliques = ensureNoOverlap(all_cliques, cliqueList)
                        elif len(neighbours) > 1:
                            for d1 in range(len(neighbours)):
                                cliqueList = [upnodeID, node, neighbours[d1]]
                                for d2 in range(d1 + 1, len(neighbours)):
                                    #if d1 + 1 == 1 and len(neighbours) == 2 and d2 == 1:
                                        #print i, j, len(subgraphs), len(subgraphs[i])
                                    if subgraphs[i][j].IsEdge(neighbours[d1], neighbours[d2]):
                                    		cliqueList.append(neighbours[d2])
                                    #elif subgraphs[i][j - 2].IsEdge(neighbours[d1], neighbours[d2]):
                                    		#cliqueList.append(neighbours[d2])
                                if len(cliqueList) >= clique_size:
                                    all_cliques = ensureNoOverlap(all_cliques, cliqueList)
                                    
                    all_cliques2 = []   
                    for node in edgeList2:
                        neighbours = edgeList2[node]
                        if len(neighbours) == 1:
                            cliqueList = [upnodeID, node, neighbours[0]]
                            if len(cliqueList) >= clique_size:
                                all_cliques2 = ensureNoOverlap(all_cliques2, cliqueList)
                        elif len(neighbours) > 1:
                            for d1 in range(len(neighbours)):
                                cliqueList = [upnodeID, node, neighbours[d1]]
                                for d2 in range(d1 + 1, len(neighbours)):
                                    #if d1 + 1 == 1 and len(neighbours) == 2 and d2 == 1:
                                        #print i, j, len(subgraphs), len(subgraphs[i])
                                    if subgraphs[i][j - 2].IsEdge(neighbours[d1], neighbours[d2]):
                                    		cliqueList.append(neighbours[d2])
                                if len(cliqueList) >= clique_size:
                                    all_cliques2 = ensureNoOverlap(all_cliques2, cliqueList)
                    
                    for q in all_cliques:
                        if len(q) == clique_size:
                            print q, " C2"
                            a1.append(q)
                            T = T + 1
                    for q in all_cliques2:
                        if len(q) == clique_size:
                            print q, " C2"
                            a1.append(q)
                            T = T + 1
                
    return T

def ensureNoOverlap(all_cliques, cliqueList):
    all_cliques.append(cliqueList)
    popList = [] 
    for d1 in range(len(all_cliques) - 1):
        if len(all_cliques[d1]) >= len(cliqueList):
            if set(cliqueList) <= set(all_cliques[d1]):
                popList.append(cliqueList)
                break
        else:
            if set(all_cliques[d1]) <= set(cliqueList):
                popList.append(all_cliques[d1])
                
    if len(popList) > 0:
        all_cliques = [x for x in all_cliques if x not in popList]
    
    return all_cliques
    

while True:
    clique_size = raw_input ("Enter the size of clique: ")
    try:
        temp = int(clique_size)
        if(temp > 0):
            break
        else:
            print("Invalid Input!") 
    except:
        print("Invalid Input!")
        
clique_size = int(clique_size)
#Threshold D
for threshold in range(0, 1):
	#Graph G
    G = snap.LoadEdgeList(snap.PUNGraph, "outt1.txt", 0, 1)
    for NI in G.Nodes():
        NID = NI.GetId()
        if G.IsEdge(NID, NID):
            G.DelEdge(NID, NID)
                    
    tStart = time.time()
    #Output the number of triangles in G
    T = algorithm(G, threshold, clique_size)
    print "Number of cliques:", T
    tEnd = time.time()
	#The time spent while we set threshold=D in the pruning step
    print "Time: ", tEnd - tStart