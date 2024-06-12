from solver_test_2 import *
import networkx as nx
import pulp as plp
import matplotlib.pyplot as plt
from common import *
from create_graph import *
from validate import *
#from pulp import Lpvariable
#import Solvers as sol 
#from sol import *
#from ILP import scip



PHY = CreatePHYGraph()
SLICE_SET = CreateSlicesSet()
problem = GraphMappingToILP(PHY, SLICE_SET)
#print(problem)
#print(PHY.nodes(data=True))
#print(PHY.edges(data=True))
#for i in SLICE_SET:
#   for j in i:
#       print(j.nodes(data=True))
#       print(j.edges(data=True))
# solver = plp.SCIP_CMD()
# solution = problem.solve(solver)
# print(value(problem.objective))
#print(problem.solve())
#print(plp.LpStatus[problem.status])
problem.solve()
#print(plp.value(problem.objective))
#print(problem.variables())
#for i in range(len(problem.variables())):
#    print(problem.variables()[i], problem.variables()[i].value())
# print("============================================================")
# xnode = [var for  var in problem.variables() if "xEdge" in var.name]
# for var in xnode:
#     print(var,"=", var.value())
print(ValidateSolution(problem, PHY, SLICE_SET))