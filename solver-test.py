import networkx as nx 
import pulp as plp 
import matplotlib.pyplot as plt


def GraphMappingToILP(PHY:nx.DiGraph, SLICE_SET:list[list[nx.DiGraph]]) -> pulp.lpProblem:
    #create values of multi sfc with multi config : list(list(node))
    #SLICE_SET_MULTI_CONFIG == SSLCE_SET
    SSLC_SET_NODES = list()
    for sfc_config_k_set in SLICE_SET:
        CONFIG_K= list()
        for sfc in sfc_config_k_set:
            CONFIG_K.append(
                plp.LpVariable.dicts(
                    name=f"xNode_{SLICE_SET.index(sfc_config_k_set)}_{sfc_config_k_set.index(sfc)}",
                    indices=(sfc.nodes, PHY.nodes),
                    cat = "Binary"
            )
        )
        SSLC_SET_NODES.append(CONFIG_K)
    #create values of multi sfc with multi config : list(list(edge))
    #SLICE_SET_MULTI_CONFIG == SSLCE_SET
    SSLC_SET_EDGES = list()
    for sfc_config_k_set in SLICE_SET:
        CONFIG_K= list()
        for sfc in sfc_config_k_set:
            CONFIG_K.append(
                plp.LpVariable.dicts(
                    name=f"xEdge_{SLICE_SET.index(sfc_config_k_set)}_{sfc_config_k_set.index(sfc)}",
                    indices=(sfc.edges, PHY.edges),
                    cat = "Binary"
            )
        )
        SSLC_SET_EDGES.append(CONFIG_K)
    
    #define variable of pi (0==no mapping,1==mapping)
    pi = plp.LpVariable(
    name="pi",
    cat=plp.LpBinary
    )
    #define the values of nodes and edges
    

    #CONSTRAINTS 1 : MOI NODE O MANG SFC DUOC MAP VAO MOT NODE O MANG VAT LY
 