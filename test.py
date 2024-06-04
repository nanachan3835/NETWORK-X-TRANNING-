from solver_test import *
import networkx as nx
import pulp as plp
import matplotlib.pyplot as plt
from common import *
from create_graph import *




PHY = CreatePHYGraph()
SLICE_SET = CreateSlicesSet()
problem = GraphMappingToILP(PHY, SLICE_SET)
print(problem)
print(PHY.nodes(data=True))
print(PHY.edges(data=True))

print(SLICE_SET[i][j](data=True) for i in range(len(SLICE_SET)) for j in range(len(SLICE_SET[i])))







