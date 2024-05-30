import networkx as nx 
import pulp as plp 
import matplotlib.pyplot as plt

# define G , G = 5 node 8 links

G = nx.DiGraph()

# add node to G
for i in range(5):
    G.add_node(i, a=10) # add node with attribute a = 10

# add links to G 
for i in range(4):
    G.add_edge(i, i+1, a=10) # add link with attribute a = 10
    G.add_edge(i+1, i, a=10) # add link with attribute a = 10

# define GS , GS = 3 node 2 links (a list of GS , 4GS)
GS_DICT = {}

for i in range(4):
    GS_DICT[i]= nx.DiGraph()
    GS_DICT[i].add_node(0, r=2)
    GS_DICT[i].add_node(1, r=2)
    GS_DICT[i].add_node(2, r=2)
    GS_DICT[i].add_edge(0,1,r=5)
    GS_DICT[i].add_edge(1,2,r=5)


print(GS_DICT[1].nodes)
print(GS_DICT[1].edges)      
print(GS_DICT[1].nodes[0]['r'])
#for test with multiple GS
#for i in range(len(GS_DICT)): 
#    change GS_DICT[0]= GS_DICT[i]
#JUST TESTING , IF WORKING THEN PACKAGING IT INTO A FUNCTION


# choose GS[0] as the input

aNode = nx.get_node_attributes(G, "a")
aEdge = nx.get_edge_attributes(G, "a")

rNode = nx.get_node_attributes(GS_DICT[0], "r")
rEdge = nx.get_edge_attributes(GS_DICT[0], "r")



# problem for G and GS[0]

problem = plp.LpProblem(name="graph-mapping", sense=plp.LpMaximize)
# define variable of nodes
xNode = plp.LpVariable.dicts(
    name="xNode",
    indices=(GS_DICT[0].nodes, G.nodes),
    cat=plp.LpBinary
)
# define variable of edges
xEdge = plp.LpVariable.dicts(
    name="xEdge",
    indices=(GS_DICT[0].edges, G.edges),
    cat=plp.LpBinary
)
# define variable of pi (0==no mapping,1==mapping)
pi = plp.LpVariable(
    name="pi",
    cat=plp.LpBinary
)


# C1
for i in G.nodes:
    problem += (
        plp.lpSum(
            xNode[j][i]*rNode[j]
            for j in GS_DICT[0].nodes
            ) <= aNode[i],
        f"C1_{i}"
    )

# C2

for i in G.edges:
    problem += (
        plp.lpSum(
            xEdge[j][i] * rEdge[j]
            for j in GS_DICT[0].edges
            ) <= aEdge[i],
        f"C2_{i}"
    )

# C3
for i in G.nodes:
    problem += (
        plp.lpSum(
            xNode[j][i] for j in GS_DICT[0].nodes
            for j in GS_DICT[0].nodes
            ) <= pi,
        f"C3_{i}"
    )
# C4
for v in GS_DICT[0].nodes:
    problem += (
        plp.lpSum(
            xNode[v][i]
            for i in G.nodes
        ) == pi,
        f"C4_{v}"
    )
#C5
for vw in GS_DICT[0].edges:
    for i in G.nodes:
        problem += (
            (
                plp.lpSum(xEdge[vw].get((i,j)) for j in G.nodes) 
                - plp.lpSum(xEdge[vw].get((j,i)) for j in G.nodes)
            ) == xNode[vw[0]][i] - xNode[vw[1]][i],
            f"C5_{i}_{vw}"
        )



print("###################")
print(xEdge[(0,1)].get(1,0))




problem += (
    plp.lpSum(
        xNode[v][i]
        for v in GS_DICT[0].nodes
        for i in G.nodes
    )
)

print(problem)

# function to make graph
def makegraph(n,r_Nodes:list,r_Edges:list):
    G= nx.DiGraph()
    for i in range(n):
        G.add_node(i, a=r_Nodes[i]) 
    for i in range(n-1):
        G.add_edge(i, i+1, a=r_Edges[i]) 
        G.add_edge(i+1, i, a=r_Edges[i]) 
    return G


GS_list={G1:makegraph(3,[2,2,2],[5,5]),G2:makegraph(3,[2,2,2],[5,5])}
print(GS_list[G1].nodes)
