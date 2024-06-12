from solver_test_2 import *
import networkx as nx
import pulp as plp
import matplotlib.pyplot as plt
from common import *
from create_graph import *

# Check_C1: Mỗi nút của mạng vật lý không vượt quá khả năng chứa
# def Check_C1(NODE_LIST:list[list[plp.LpVariable]],PHY:nx.DiGraph,SLICE_SET:list[list[nx.DiGraph]]):
#     # rang buoc 1
#     for node in PHY.nodes:
#         if not (
#             sum(
#                 sum(
#                     NODE_LIST[s][k][node_S].value() * nx.get_node_attributes(SLICE_SET[s][k], "req")[node_S]
#                     for node_S in SLICE_SET[s][k].nodes
#                 )
#                 for s in range(len(SLICE_SET))
#                 for k in range(len(SLICE_SET[s]))
#             )
#                 <= nx.get_node_attributes(PHY, "cap")[node]
#         ):
#             return False
#     return True
# # Check_C2: Mỗi cạnh của mạng vật lý không vượt quá khả năng chứa
# def Check_C2(EDGE_LIST:list[list[plp.LpVariable]],PHY:nx.DiGraph,SLICE_SET:list[list[nx.DiGraph]]):
#     # rang buoc 2
#     for edge in PHY.edges:
#         if not (
#             sum(
#                 sum(
#                     EDGE_LIST[s][k][edge_S][edge].value() * nx.get_edge_attributes(SLICE_SET[s][k], "req")[edge_S]
#                     for edge_S in SLICE_SET[s][k].edges
#                 )
#                 for s in range(len(SLICE_SET))
#                 for k in range(len(SLICE_SET[s]))
#             )
#                 <= nx.get_edge_attributes(PHY, "cap")[edge]
#         ):
#             return False
#     return True
# #check C3: 
# def Check_C3(NODE_LIST:list[list[plp.LpVariable]],PHY:nx.DiGraph,SLICE_SET:list[list[nx.DiGraph]],z:list[plp.LpVariable]):
#     for s in range(len(SLICE_SET)):
#         for k in range(len(SLICE_SET[s])):
#             if not (
#                 sum(
#                     sum(
#                         NODE_LIST[s][k][node_S][node].value() * nx.get_node_attributes(SLICE_SET[s][k], "req")[node_S]
#                         for node_S in SLICE_SET[s][k].nodes
#                     )
#                     for node in PHY.nodes
#                 )
#                     <= z[s][k].value()
#             ):
#                 return False 
#     return True
# #check C4:
# def Check_C4(NODE_LIST:list[list[plp.LpVariable]],PHY:nx.DiGraph,SLICE_SET:list[list[nx.DiGraph]],z:list[list[plp.LpVariable]]):
#     for s in range(len(SLICE_SET)):
#         for k in range(len(SLICE_SET[s])):
#             for node in SLICE_SET[s][k].nodes:
#                 if not (
#                     sum(
#                         NODE_LIST[s][k][node_S][node].value()
#                         for node_S in PHY.nodes
#                     )
#                         == z[s][k].value()
#                 ):
#                     return False
#     return True
# #check C5:
# def Check_C5(NODE_LIST:list[list[plp.LpVariable]],EDGE_LIST:list[list[plp.LpVariable]],PHY:nx.DiGraph,SLICE_SET:list[list[nx.DiGraph]],phi:list[list[plp.LpVariable]]):
#     for s in range(len(SLICE_SET)):
#         for k in range(len(SLICE_SET[s])):
#             for node in PHY.nodes:
#                 for edge in SLICE_SET[s][k].edges:
#                     if not (
#                         sum(
#                             sum(
#                                 EDGE_LIST[s][k][edge_S][edge].value() - EDGE_LIST[s][k][edge_S[::-1]][edge]
#                                 for edge_S in PHY.edges if edge_S[0] == node
#                             )
#                             - (NODE_LIST[s][k][edge[0]][node].value() - NODE_LIST[s][k][edge[1]][node].value())
#                         )
#                             <= 100 * (1 - phi[s][k].value())
#                     ):
#                         return False
#                     if not (
#                         sum(
#                             sum(
#                                 EDGE_LIST[s][k][edge_S][edge].value() - EDGE_LIST[s][k][edge_S[::-1]][edge]
#                                 for edge_S in PHY.edges if edge_S[0] == node
#                             )
#                             - (NODE_LIST[s][k][edge[0]][node].value() - NODE_LIST[s][k][edge[1]][node].value())
#                         )
#                             >= -100 * (1 - phi[s][k].value())
#                     ):
#                         return False
#     return True
# #check C6:
# def Check_C6(SLICE_SET:list[list[nx.DiGraph]],phi:list[list[plp.LpVariable]],pi:list[plp.LpVariable]):
#     if not (
#         sum(
#             phi[s][k].value()
#             for k in range(len(SLICE_SET[s]))
#             for s in range(len(SLICE_SET))
#         )
#             == pi[s].value() for s in range(len(SLICE_SET))
#     ):
#         return False
#     return True
# #check C7:
# def Check_C7(SLICE_SET:list[list[nx.DiGraph]],phi:list[list[plp.LpVariable]],pi:list[plp.LpVariable],z:list[list[plp.LpVariable]]):
#     for s in range(len(SLICE_SET)):
#         for k in range(len(SLICE_SET[s])):
#             if not (
#                 z[s][k].value()
#                     <= pi[s].value()
#             ):
#                 return False
#             if not (
#                 z[s][k].value()
#                     <= phi[s][k].value()
#             ):
#                 return False
#             if not (
#                 z[s][k].value()
#                     >= pi[s].value() + phi[s][k].value() - 1
#             ):
#                 return False
#     return True
#function gen nodelist()
def GenNodeList(problem:plp.LpProblem,SLICE_SET:list[list[nx.DiGraph]]) -> list[list[plp.LpVariable]]:
    xNode = dict()
    for s in range(len(K)):
        xNode[s]=dict()
        for k in range(len(K[s])):
            xNode[s][k]=dict()
            for i in PHY.nodes:
                xNode[s][k][i] = dict()
                for v in K[s][k].nodes:
                    xNode[s][k][i][v] = solution_data[f"xNode_{s}_{k}_({v},_{i})"]
    return xNode
#function gen edgelist()
def GenEdgeList(problem:plp.LpProblem,SLICE_SET:list[list[nx.DiGraph]]) -> list[list[plp.LpVariable]]:
    for s in range(len(K)):
        xEdge[s]=dict()
        for k in range(len(K[s])):
            xEdge[s][k]=dict()
            for (i,j) in PHY.edges:
                xEdge[s][k][(i,j)] = dict()
                for (v,w) in K[s][k].edges:
                    xEdge[s][k][(i,j)][(v,w)] = solution_data[f"xEdge_{s}_{k}_(({v},_{w}),_({i},_{j}))"]
#function gen phi()
def GenPhi(problem:plp.LpProblem,SLICE_SET:list[list[nx.DiGraph]]) -> list[list[plp.LpVariable]]:
    phi = dict()
    for s in range(len(K)): 
        phi[s] = dict()
        for k in range(len(K[s])):
            phi[s][k]=solution_data[f"phi_{s}_{k}"]
    return phi
#function gen pi()
def GenPi(problem:plp.LpProblem) -> list[plp.LpVariable]:
    pi = dict()
    for s in range(len(K)):
        pi[s] = solution_data[f"pi_{s}"]
    return pi
#function gen z()
def GenZ(problem:plp.LpProblem,SLICE_SET:list[list[nx.DiGraph]]) -> list[list[plp.LpVariable]]:
    z = dict()
    for s in range(len(K)): 
        z[s] = dict()
        for k in range(len(K[s])):
            z[s][k]=solution_data[f"z_{s}_{k}"]
    return z

#check Objective Function
def ValidateSolution(problem:plp.LpProblem,PHY:nx.DiGraph,SLICE_SET=list[list[nx.DiGraph]]):
    NODE_LIST = GenNodeList(problem,SLICE_SET)
    EDGE_LIST = GenEdgeList(problem,SLICE_SET)
    phi = GenPhi(problem,SLICE_SET)
    pi = GenPi(problem)
    z = GenZ(problem,SLICE_SET)
    if not Check_C1(NODE_LIST,PHY,SLICE_SET):
        return False
    if not Check_C2(EDGE_LIST,PHY,SLICE_SET):
        return False
    if not Check_C3(NODE_LIST,EDGE_LIST,PHY,SLICE_SET,z):
        return False
    if not Check_C4(NODE_LIST,EDGE_LIST,PHY,SLICE_SET,z):
        return False
    if not Check_C5(NODE_LIST,EDGE_LIST,PHY,SLICE_SET,phi):
        return False
    if not Check_C6(SLICE_SET,phi,pi):
        return False
    if not Check_C7(SLICE_SET,phi,pi,z):
        return False
    return True