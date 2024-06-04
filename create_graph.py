import networkx as nx
import random   



def generate_config_slice():

    # Create a list of configuration
    GS = list()

    # Create 4 configuration of a slice
    k1 = nx.DiGraph()
    k1.add_node(0,r=random.randint(20,25))
    k1.add_node(1,r=random.randint(20,25))
    k1.add_node(2,r=random.randint(20,25))

    k1.add_edge(0,1,r=random.randint(20,25))
    k1.add_edge(1,2,r=random.randint(20,25))
    
    GS.append(k1)

    k2 = nx.DiGraph()
    k2.add_node(0,r=random.randint(15,20))
    k2.add_node(1,r=random.randint(15,20))
    k2.add_node(2,r=random.randint(15,20))
    k2.add_node(3,r=random.randint(15,20))

    k2.add_edge(0,1,r=random.randint(15,20))
    k2.add_edge(1,2,r=random.randint(15,20))
    k2.add_edge(2,3,r=random.randint(15,20))

    GS.append(k2)

    #k3 = nx.DiGraph()
    #k3.add_node(0,r=random.randint(10,15))
    #k3.add_node(1,r=random.randint(10,15))
    #k3.add_node(2,r=random.randint(10,15))
    #k3.add_node(3,r=random.randint(10,15))

    #k3.add_edge(0,1,r=random.randint(10,15))
    #k3.add_edge(1,2,r=random.randint(10,15))
    #k3.add_edge(1,3,r=random.randint(10,15))
    
    # GS.append(k3)

    # k4 = nx.DiGraph()
    # k4.add_node(0,r=random.randint(5,10))
    # k4.add_node(1,r=random.randint(5,10))
    # k4.add_node(2,r=random.randint(5,10))
    # k4.add_node(3,r=random.randint(5,10))

    # k4.add_edge(0,1,r=random.randint(5,10))
    # k4.add_edge(1,2,r=random.randint(5,10))
    # k4.add_edge(2,3,r=random.randint(5,10))
    # k4.add_edge(3,0,r=random.randint(5,10))

    # GS.append(k4)

    return GS


def CreatePHYGraph():
    PHY = nx.DiGraph()

    # Create a physical network PHY
    for i in range(9):
        PHY.add_node(i,a=random.randint(10,30))

    for i in range(7):
            r = random.randint(10,30)
            PHY.add_edge(i,i+1,a=r)
            PHY.add_edge(i+1,i,a=r)
    
    r = random.randint(10,30)
    PHY.add_edge(8,6,a=r)
    PHY.add_edge(6,8,a=r)
    PHY.add_edge(5,1,a=r)
    PHY.add_edge(1,5,a=r)



    return PHY

def CreateSlicesSet():
    # Create a list of slices
    K = list()
    for i in range(2):
        # Create a list of configuration for each slice
        K.append(generate_config_slice())

    return K