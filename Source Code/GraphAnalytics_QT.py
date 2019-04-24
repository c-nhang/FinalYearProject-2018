import sys
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from graphviz import Graph
import tkinter as tk
import snap
import time
import functools
import operator
import copy

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setGeometry(100, 100, 1350, 900)
        self.setWindowTitle("Graph Analytics Software")
        self.setAutoFillBackground(True)
        self.bgColor = self.palette()
        self.bgColor.setColor(self.backgroundRole(), QColor(204,211,251))
        self.setPalette(self.bgColor)
        
        self.title = QtGui.QLabel(self)
        self.title.setText("Graph Analytics Software")
        self.title.setStyleSheet('font: 40px Courier New; color: black; font-weight:bold;')
        self.title.move(15,15)
        
        self.edgeListLabel = QtGui.QLabel(self)
        self.edgeListLabel.setText("Edge List:")
        self.edgeListLabel.setStyleSheet('font: 30px Courier New; color: black; font-weight:bold;')
        self.edgeListLabel.move(15,90)
        
        self.uploadBtn = QPushButton("Choose File", self)
        self.uploadBtn.clicked.connect(self.selectFile)
        self.uploadBtn.move(210,90)
        self.uploadBtn.setStyleSheet('width: 230px; background-color: #FDEB42; font: 30px Courier New; color: #004C70; font-weight:bold; border-radius: 15px;')
        
        self.filePath = QtGui.QLabel("--No File--", self)
        self.filePath.setStyleSheet('font: 30px Courier New; color: black; font-weight:bold;')
        self.filePath.move(460,90)
        self.filePath.setFixedWidth(1400)
        
        self.cliqueSizeLabel = QtGui.QLabel(self)
        self.cliqueSizeLabel.setText("Clique Size:")
        self.cliqueSizeLabel.setStyleSheet('font: 30px Courier New; color: black; font-weight:bold;')
        self.cliqueSizeLabel.move(15,140)
        
        self.cliqueSizeTextbox = QLineEdit(self)
        self.cliqueSizeTextbox.move(245, 140)
        self.cliqueSizeTextbox.resize(70,35)
        
        self.submitBtn = QPushButton("OK", self)
        self.submitBtn.clicked.connect(self.calculate)
        self.submitBtn.move(335,140)
        self.submitBtn.setStyleSheet('width: 55px; background-color: #C1C1C1; font: 30px Courier New; color: white; font-weight:bold; border-radius: 15px;')
        
        self.cliqueNumLabel = QtGui.QLabel(self)
        self.cliqueNumLabel.setText("Number of Cliques:")
        self.cliqueNumLabel.setStyleSheet('font: 30px Courier New; color: black; font-weight:bold;')
        self.cliqueNumLabel.move(15,190)
        
        self.cliqueNum = QtGui.QLabel(self)
        self.cliqueNum.setText("0")
        self.cliqueNum.setStyleSheet('font: 30px Courier New; color: black; font-weight:bold;')
        self.cliqueNum.move(350,190)
        
        self.dict = {}
        
        self.edgeList = []
        
        self.window = QWidget(self)
        self.canvasArea = QScrollArea()
        self.graphVis = QtGui.QLabel(self.window)
        self.canvasArea.setWidget(self.graphVis)
        self.layout = QVBoxLayout(self.window) 
        self.layout.addWidget(self.canvasArea)

        self.screenWidth = tk.Tk().winfo_screenwidth() - 200
        self.screenHeight = tk.Tk().winfo_screenheight() - 250
        
        self.window.setGeometry(10, 220, tk.Tk().winfo_screenwidth() - 10, tk.Tk().winfo_screenheight() - 295)
        self.shortName = ""
        self.showMaximized()
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        
        self.allCliques = []
        self.new_list = []
        
    def selectFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '.')
        self.readFile(filename)
        
    def calculate(self):
        if self.shortName == "--No File--" or self.shortName == "":
            self.showDialog()
        elif self.cliqueSizeTextbox.text() == "" or self.cliqueSizeTextbox.text() == 0:
            self.showDialog2()
        else: 
            clique_size = self.cliqueSizeTextbox.text()
            try:
                temp = int(clique_size)
                if(temp > 0):
                    clique_size = int(clique_size)
                    G = snap.LoadEdgeList(snap.PUNGraph, self.shortName, 0, 1)
                    for NI in G.Nodes():
                        NID = NI.GetId()
                        if G.IsEdge(NID, NID):
                            G.DelEdge(NID, NID)
                    self.allCliques = []
                    T = self.algorithm(G, 3, clique_size)
                    print "Number of cliques:", T
                    self.cliqueNum.setText(str(T))
                    self.drawGraph()

                else:
                    self.showDialog3()
            except Exception as e:
                print (e)
                self.showDialog3()
        
    def showDialog2(self):
        d = QDialog(self, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        b1 = QPushButton("OK",d)
        b1.move(200,125)
        b1.clicked.connect(d.accept)
        t1 = QLabel("Clique Size should not be empty", d)
        t1.setStyleSheet('font: 22px Courier New; color: black; font-weight:bold;')
        t1.move(50,18)
        t2 = QLabel("or equal to zero", d)
        t2.setStyleSheet('font: 22px Courier New; color: black; font-weight:bold;')
        t2.move(150,50)
        d.setWindowTitle("Warning")
        d.setWindowModality(Qt.ApplicationModal)
        d.resize(500,170)
        d.setAutoFillBackground(True)
        d.bgColor = d.palette()
        d.bgColor.setColor(d.backgroundRole(), QColor(225,225,225))
        d.setPalette(d.bgColor)
        d.setFixedSize(500, 170)
        d.exec_()
        
    def showDialog3(self):
        d = QDialog(self, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        b1 = QPushButton("OK",d)
        b1.move(200,125)
        b1.clicked.connect(d.accept)
        t1 = QLabel("Invalid Input!", d)
        t1.setStyleSheet('font: 30px Courier New; color: black; font-weight:bold;')
        t1.move(130,45)
        d.setWindowTitle("Warning")
        d.setWindowModality(Qt.ApplicationModal)
        d.resize(500,170)
        d.setAutoFillBackground(True)
        d.bgColor = d.palette()
        d.bgColor.setColor(d.backgroundRole(), QColor(225,225,225))
        d.setPalette(d.bgColor)
        d.setFixedSize(500, 170)
        d.exec_()
    
    def readFile(self, filename):
        filename = str(filename)
        index = filename.rfind("/") + 1
        self.shortName = filename[index:len(filename)]
        self.dict = {}
        self.edgeList = []
        try:
            with open(filename) as fileIn:
                for line in fileIn:
                    nodeId, neighbourId = [int(s) for s in line.split()]
                    if nodeId not in self.dict:
                        self.dict[nodeId] = [neighbourId]
                    else:
                        self.dict[nodeId].append(neighbourId)
            if len(self.shortName) > 25:
                self.shortName = self.shortName[0:25] + "..."
            self.ensureBidirectional()
            self.drawGraph()
        except Exception as e: 
            #print(e)
            if (not self.shortName == ""):
                self.showDialog()
            self.shortName = "--No File--"
        finally:
            self.filePath.setText(self.shortName)
        
    def ensureBidirectional(self):
        for nodeId in self.dict.keys():
            neighbourList = self.dict[nodeId]
            for neighbourId in neighbourList:
                if neighbourId not in self.dict:
                    self.dict[neighbourId] = [nodeId]
                elif nodeId not in self.dict[neighbourId]:
                    self.dict[neighbourId].append(nodeId)
    
    def drawGraph(self):
        self.edgeList = []
        g = Graph('G', filename='graph.gv', engine='neato', format='png', edge_attr={'color':'black', 'style':'filled', 'len':'1.5'}, graph_attr={'bgcolor':'transparent', 'overlap':'scale', 'splines':'true', 'center':'true'}, node_attr={'fontcolor': 'black', 'fontname':'bold', 'color':' black', 'style':'filled', 'fillcolor':'white'})
        if len(self.allCliques) > 0:
            self.new_list = copy.copy(self.allCliques)
            self.allCliques = functools.reduce(operator.concat, self.allCliques)
        else:
            g.attr('edge', style='filled', color='black')
        for nodeId in self.dict.keys():
            if nodeId in self.allCliques:
                g.attr('node', style='filled', color='#A70000', fillcolor='red')
            else:
                g.attr('node', style='filled', color='black', fillcolor='white')
            g.node(str(nodeId))
            neighbourList = self.dict[nodeId]
            for neighbourId in neighbourList:
                if neighbourId in self.allCliques:
                    g.attr('node', style='filled', color='#A70000', fillcolor='red')
                else:
                    g.attr('node', style='filled', color='black', fillcolor='white')
                g.node(str(neighbourId))
                if (not self.edgeExist(nodeId, neighbourId)):
                    if self.ensureSameClique(nodeId, neighbourId) and nodeId in self.allCliques and neighbourId in self.allCliques:
                        g.attr('edge', style='filled', color='#B40000')
                    else:
                        g.attr('edge', style='filled', color='black')
                    g.edge(str(nodeId), str(neighbourId))
        g.render()
        pixmap = QPixmap("graph.gv.png")
        self.graphVis.setPixmap(pixmap)
        self.graphVis.adjustSize()

    def ensureSameClique(self, src, dst):
        for list1 in self.new_list:
            if src in list1 and dst in list1:
                return True
        return False
            
    def edgeExist(self, src, dst):
        for edge in self.edgeList:
            if ((src in edge) and (dst in edge)):
                return True        
        self.edgeList.append([src, dst])
        return False
        
    def showDialog(self):
        d = QDialog(self, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        b1 = QPushButton("OK",d)
        b1.move(200,125)
        b1.clicked.connect(d.accept)
        t1 = QLabel("Edge List must be a text file (.txt)", d)
        t1.setStyleSheet('font: 22px Courier New; color: black; font-weight:bold;')
        t1.move(18,18)
        t2 = QLabel("and contain only two columns", d)
        t2.setStyleSheet('font: 22px Courier New; color: black; font-weight:bold;')
        t2.move(60,50)
        t3 = QLabel("(source node, destination node)!", d)
        t3.setStyleSheet('font: 22px Courier New; color: black; font-weight:bold;')
        t3.move(40,80)
        d.setWindowTitle("Warning")
        d.setWindowModality(Qt.ApplicationModal)
        d.resize(500,170)
        d.setAutoFillBackground(True)
        d.bgColor = d.palette()
        d.bgColor.setColor(d.backgroundRole(), QColor(225,225,225))
        d.setPalette(d.bgColor)
        d.setFixedSize(500, 170)
        d.exec_()
        
    def algorithm(self, G, threshold, clique_size):
        #Pruning Step
        P = 1
        T = 0
        all_cliques = []
        while P == 1:
            P = 0 
            for NI in G.Nodes():
                NID = NI.GetId()
                d = NI.GetDeg()
                
                edgeList = {}
                if d <= threshold and d >= clique_size - 1:
                    neighbours = []
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
                                all_cliques = self.ensureNoOverlap(all_cliques, cliqueList)
                        elif len(neighbours) > 1:
                            for i in range(len(neighbours) - 1):
                                cliqueList = [NID, node, neighbours[i]]
                                for j in range(i + 1, len(neighbours)):
                                    if G.IsEdge(neighbours[i], neighbours[j]):
                                    		cliqueList.append(neighbours[j])
                                if len(cliqueList) >= clique_size:
                                    all_cliques = self.ensureNoOverlap(all_cliques, cliqueList)
         
                if d <= threshold or d < clique_size - 1:
                    P = 1
                    G.DelNode(NID)
    
        for q in all_cliques:
            if len(q) == clique_size:
                print q, " Pruning"
                self.allCliques.append(q)
                T = T + 1
    
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
                    for node in edgeList:
                        neighbours = edgeList[node]
                        if len(neighbours) == 1:
                            cliqueList = [NID, node, neighbours[0]]
                            if len(cliqueList) >= clique_size:
                                all_cliques = self.ensureNoOverlap(all_cliques, cliqueList)
                        elif len(neighbours) > 1:
                            for d1 in range(len(neighbours) - 1):
                                cliqueList = [NID, node, neighbours[d1]]
                                for d2 in range(d1 + 1, len(neighbours)):
                                    if G.IsEdge(neighbours[d1], neighbours[d2]):
                                    		cliqueList.append(neighbours[d2])
                                if len(cliqueList) >= clique_size:
                                    all_cliques = self.ensureNoOverlap(all_cliques, cliqueList)               

                for q in all_cliques:
                    if len(q) == clique_size:
                        print q, " C1"
                        self.allCliques.append(q)
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
                                        
                        for s in range(len(L)):
                            for t in range(s + 1, len(L)):
                                if subgraphs[i][j - 2].IsEdge(L[s], L[t]):
                                    if L[s] not in edgeList:
                                        edgeList[L[s]] = [L[t]]
                                    else:
                                        edgeList[L[s]].append(L[t])
                                            
                        all_cliques = []   
                        for node in edgeList:
                            neighbours = edgeList[node]
                            if len(neighbours) == 1:
                                cliqueList = [upnodeID, node, neighbours[0]]
                                if len(cliqueList) >= clique_size:
                                    all_cliques = self.ensureNoOverlap(all_cliques, cliqueList)
                            elif len(neighbours) > 1:
                                for d1 in range(len(neighbours) - 1):
                                    cliqueList = [upnodeID, node, neighbours[d1]]
                                    for d2 in range(d1 + 1, len(neighbours)):
                                        if subgraphs[i][j].IsEdge(neighbours[d1], neighbours[d2]):
                                        		cliqueList.append(neighbours[d2])
                                        elif subgraphs[i][j - 2].IsEdge(neighbours[d1], neighbours[d2]):
                                        		cliqueList.append(neighbours[d2])
                                    if len(cliqueList) >= clique_size:
                                        all_cliques = self.ensureNoOverlap(all_cliques, cliqueList)
    
                        for q in all_cliques:
                            if len(q) == clique_size:
                                print q, " C2"
                                self.allCliques.append(q)
                                T = T + 1
                    
        return T
    
    def ensureNoOverlap(self, all_cliques, cliqueList):
        all_cliques.append(cliqueList)
        popList = [] 
        for d1 in range(len(all_cliques) - 1):
            if len(all_cliques[d1]) >= len(cliqueList):
                if set(cliqueList) <= set(all_cliques[d1]):
                    popList.append(cliqueList)
            else:
                if set(all_cliques[d1]) <= set(cliqueList):
                    popList.append(all_cliques[d1])
        all_cliques = [x for x in all_cliques if x not in popList]
        
        return all_cliques
        
def main():
    app = QtGui.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
	
if __name__ == '__main__':
    main()