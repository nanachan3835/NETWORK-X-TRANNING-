import pulp as plp 
import matplotlib.pyplot as plt
import math
import networkx as nx
from common import *

def GraphMappingToILP(PHY:nx.DiGraph, SLICE_SET:list[list[nx.DiGraph]]) -> plp.LpProblem:
    # tao problem 
    problem = plp.LpProblem(name="GraphMapping", 
                            sense=plp.LpMaximize)
    # tao bien xNode

    xNode = plp.LpVariable.dicts(name="xNode",
                                 indices = [(s,k,i,v) for i in PHY.nodes
                                             for s in range(len(SLICE_SET))
                                             for k in range(len(SLICE_SET[s]))
                                             for v in SLICE_SET[s][k].nodes],
                                 cat=plp.LpBinary)
    # tao bien xEdge
    xEdge = plp.LpVariable.dicts(name="xEdge",
                                 indices = [(s,k,(i,j),(v,w)) for s in range(len(SLICE_SET))
                                             for k in range(len(SLICE_SET[s]))
                                             for (i,j) in PHY.edges
                                             for (v,w) in SLICE_SET[s][k].edges],
                                 cat=plp.LpBinary)
    # tao bien phi
    phi = plp.LpVariable.dicts(name="phi",
                               indices = [(s,k) for s in range(len(SLICE_SET))
                                           for k in range(len(SLICE_SET[s]))],
                               cat=plp.LpBinary)
    # tao bien pi
    pi = plp.LpVariable.dicts(name="pi",
                              indices = [s for s in range(len(SLICE_SET))],
                              cat=plp.LpBinary)
    # tao bien z    
    z = plp.LpVariable.dicts(name="z",
                             indices = [(s,k) for s in range(len(SLICE_SET))
                                         for k in range(len(SLICE_SET[s]))],
                             cat=plp.LpBinary)
    #PHY_add = 
   


    # tao cac rang buoc
    # rang buoc 1
    for i in PHY.nodes: 
            problem += plp.lpSum(
                                 xNode[(s,k,i,v)] * SLICE_SET[s][k].nodes[v]["r"]
                                 for s in range(len(SLICE_SET))
                                 for k in range(len(SLICE_SET[s]))
                                 for v in SLICE_SET[s][k].nodes
                                 ) <= PHY.nodes[i]["a"], f"C1_{i}"
            #) <= nx.get_node_attributes(PHY.nodes[i],"a"), f"C1_{i}"
    # rang buoc 2
   
    for (i,j) in PHY.edges:
            problem += plp.lpSum(xEdge[(s,k,(i,j),(v,w))] 
                                 for s in range(len(SLICE_SET))
                                 for k in range(len(SLICE_SET[s]))
                                 for (v,w) in SLICE_SET[s][k].edges
                                 ) <= PHY.edges[(i,j)]["a"], f"C2_{(i,j)}"
            #) <= nx.get_edge_attributes(PHY.edge[i,j],"a"), f"C2_{(i,j)}"
    # rang buoc 3
    for s in range(len(SLICE_SET)):
        for k in range(len(SLICE_SET[s])):
            for i in PHY.nodes:
                problem += plp.lpSum(xNode[(s,k,i,v)]  
                             for v in SLICE_SET[s][k].nodes
                             ) <= z[(s,k)], f"C3_{s}_{k}_{i}"
                             
    # rang buoc 4
    for s in range(len(SLICE_SET)):
        for k in range(len(SLICE_SET[s])):
            for v in SLICE_SET[s][k].nodes:
                problem += plp.lpSum(xNode[(s,k,i,v)] 
                                     for i in PHY.nodes
                                     ) == z[(s,k)], f"C4_{s}_{k}_{v}"
    # rang buoc 5
    for s in range(len(SLICE_SET)):
        for k in range(len(SLICE_SET[s])):
            for i in PHY.nodes:
                for (v,w) in SLICE_SET[s][k].edges:
                    problem += plp.lpSum(xEdge[(s,k,(i,j),(v,w))]-xEdge[(s,k,(j,i),(v,w))]
                                        for j in PHY.nodes if (i,j) in PHY.edges) - (xNode[(s,k,i,v)] - xNode[(s,k,i,w)]) <= 100*(1-phi[(s,k)]), f"C5_1_{s}_{k}_{i}_{(v,w)}"
                    problem += plp.lpSum(xEdge[(s,k,(i,j),(v,w))]-xEdge[(s,k,(j,i),(v,w))]
                                        for j in PHY.nodes if (i,j) in PHY.edges) - (xNode[(s,k,i,v)] - xNode[(s,k,i,w)]) >= -100*(1-phi[(s,k)]), f"C5_2_{s}_{k}_{i}_{(v,w)}"

    # rang buoc 6
    for s in range(len(SLICE_SET)):
            problem += plp.lpSum(phi[(s,k)] 
                                 for k in range(len(SLICE_SET[s])) 
                                 for s in range(len(SLICE_SET))
                                 ) == pi[s],f"C6_{s}"
    # rang buoc 7
    for s in range(len(SLICE_SET)):
        for k in range(len(SLICE_SET[s])):
            problem += z[(s,k)] <= pi[s], f"C7_1_{s}_{k}"
            problem += z[(s,k)] <= phi[(s,k)], f"C7_2_{s}_{k}"
            problem += z[(s,k)] >= pi[s] + phi[(s,k)] - 1, f"C7_3_{s}_{k}"
    #OBJECTIVE FUNCTION
    problem += plp.lpSum(pi[s] for s in range(len(SLICE_SET))) - (1-0.999)*(plp.lpSum(xEdge[(s,k,(i,j),(v,w))] 
                                                                               for s in range(len(SLICE_SET)) 
                                                                               for k in range(len(SLICE_SET[s]))
                                                                               for (i,j) in PHY.edges
                                                                               for (v,w) in SLICE_SET[s][k].edges))
    return problem