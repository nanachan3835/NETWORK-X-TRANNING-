import networkx as nx 
import pulp as plp 
import matplotlib.pyplot as plt
import math 


def GraphMappingToILP(PHY:nx.DiGraph, SLICE_SET:list[list[nx.DiGraph]]) -> plp.LpProblem:
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
    #define variable of PHI (0==choosent,1==choose)
    phi_list_list = list()
    for sfc_config_k_set in SLICE_SET:
        phi_list = list()
        for sfc in sfc_config_k_set:
            phi = plp.LpVariable(
                name="phi",
                cat=plp.LpBinary
            )
            phi_list.append(phi)
        phi_list_list.append(phi_list)
    #define the values of nodes and edges
    #define the values :list(list(node))
    rNODES = list()
    for sfc_config_k_set in SLICE_SET:
        CONFIG_K= list()
        for sfc in sfc_config_k_set:
            attributes_sfc = nx.get_node_attributes(sfc, "req")
            CONFIG_K.append(attributes_sfc)
        rNODES.append(CONFIG_K)
    #define the values :list(list(edge))
    rEDGES = list()
    for sfc_config_k_set in SLICE_SET:
        CONFIG_K= list()
        for sfc in sfc_config_k_set:
            attributes_sfc = nx.get_edge_attributes(sfc, "req")
            CONFIG_K.append(attributes_sfc)
        rEDGES.append(CONFIG_K)      

    #CONSTRAINTS 1 : MOI NODE O MANG SFC DUOC MAP VAO MOT NODE O MANG VAT LY
    for node in PHY.nodes:
        sum_node = 0
        for sfc_config_k_set in SLICE_SET:
            for sfc in sfc_config_k_set:
                sum_node += plp.lpSum(
                    plp.lpSum(
                        SSLC_SET_NODES[i][j][(node_S,node)] for i in range(len(SSLC_SET_NODES)) for j in range(len(SSLC_SET_NODES[i]))
                        * rNODES[SSLC_SET_NODES.index(sfc_config_k_set)][sfc_config_k_set.index(sfc)][node_S]
                        for node_S in sfc.nodes
                    )
                )
        __problem += (
            sum_node <= nx.get_node_attributes(PHY, "cap")[node] * pi, 
            f"C1_i{node}"
        )
    #CONSTRAINTS 2 : MOI LINK O MANG VAT LY DUOC MAP VAO MOT LINK O MANG VAT LY
    for edge in PHY.edges:
        sum_edge = 0
        for sfc_config_k_set in SLICE_SET:
            for sfc in sfc_config_k_set:
                sum_edge += plp.lpSum(
                    plp.lpSum(
                        SSLC_SET_EDGES[i][j][(link_S,edge)] for i in range(len(SSLC_SET_EDGES)) for j in range(len(SSLC_SET_EDGES[i]))
                        * rEDGES[SSLC_SET_EDGES.index(sfc_config_k_set)][sfc_config_k_set.index(sfc)][link_S]
                        for link_S in sfc.edges
                    )
                )
        __problem += (
            sum_edge <= nx.get_edge_attributes(PHY, "cap")[edge] * pi, 
            f"C2_i{edge}"
        )
    #CONSTRAINTS 3 : MOI NODE SFC SE DUOC MAP VAO MOT NODE VAT LY
    for sfc_config_k_set in SLICE_SET:
        for sfc in sfc_config_k_set:
            for node in PHY.nodes:
                __problem += (
                    plp.lpSum(
                        SSLC_SET_NODES[i][j][(node,node_PHY)] 
                        for node in sfc.nodes
                        for i in range(len(SSLC_SET_NODES))
                        for j in range(len(SSLC_SET_NODES[i]))

                    ) <= pi,
                    f"C3_i{node}"
                )
    #CONSTRAINTS 4 : MOI NODE VAT LY SE DUOC MAP VAO MOT NODE SFC
    for sfc_config_k_set in SLICE_SET:
        for sfc in sfc_config_k_set:
            for node_S in sfc.nodes:
                __problem += (
                    plp.lpSum(
                        SSLC_SET_NODES[i][j][(node_S,node)]
                        for i in range(len(SSLC_SET_NODES))
                        for j in range(len(SSLC_SET_NODES[i])) 
                        for node in PHY.nodes
                    ) == pi,
                    f"C4_i{node}"
                )
    #CONSTRAINTS 5 : DAM BAO CHIEU CUA LINK TRONG SFC TREN  MANG VAT LY
    for sfc_config_k_set in SLICE_SET:
        for sfc in sfc_config_k_set:
            for edge in sfc.edges:
                for node in PHY.nodes:
                    __problem += (
                        abs(plp.lpSum(
                        (
                             plp.lpSum(SSLC_SET_EDGES[i][j][(link_S,edge)].get((node,node_PHY)) 
                                  for node_PHY in PHY.nodes 
                                  for i in range(len(SSLC_SET_EDGES)) 
                                  for j in range(len(SSLC_SET_EDGES[i])))
                            - plp.lpSum(SSLC_SET_EDGES[i][j][(link_S,edge)].get((node_PHY,node)) 
                                  for node_PHY in PHY.nodes 
                                  for i in range(len(SSLC_SET_EDGES)) 
                                  for j in range(len(SSLC_SET_EDGES[i])))
                        )
                        -
                        (
                            plp.lpSum(SSLC_SET_NODES[i][j][(node,node_PHY)].get((node,node_PHY)) 
                                  for node_PHY in PHY.nodes 
                                  for i in range(len(SSLC_SET_NODES)) 
                                  for j in range(len(SSLC_SET_NODES[i])))
                            - plp.lpSum(SSLC_SET_NODES[i][j][(node_PHY,node)].get((node_PHY,node))
                                    for node_PHY in PHY.nodes 
                                    for i in range(len(SSLC_SET_NODES)) 
                                    for j in range(len(SSLC_SET_NODES[i])))
                        )
                    ) 
                ) <= abs(1000*(1-phi_list_list(phi_list.index(sfc_config_k_set.index(sfc)))),
                        f"C5_i{node}_{edge}"
            )
        )
    #CONSTRAINTS 6 : CHỌN 1 CONFIG CHO k
    for sfc_config_k_set in SLICE_SET:
        for sfc in sfc_config_k_set:
            __problem += (
                plp.lpSum(phi_list_list[SLICE_SET.index(sfc_config_k_set)][sfc_config_k_set.index(sfc)]
                         ) == pi ,
                f"C6_i{SLICE_SET.index(sfc_config_k_set)}"
            )
        return __problem