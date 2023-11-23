import networkx as nx
import matplotlib.pyplot as plt
from scipy import spatial
import random


def generate_random_network_tree(N: int, K: int, edge_dim: int) -> nx.Graph:
    """
    Function to generate a random network tree with k flows
    :param 
        N: number of nodes in the tree network
        K: number of flows in the tree network
        edge_dim: dimension of the edge of the square where the network is located
    :return
        Tree: random network tree with k flows
    """
    Tree = nx.random_tree(N)

    # Generate random sources and destinations for each flow
    Tree.graph['K'] = K

    for node in Tree.nodes():
        # pos corrisponde alle coordinate cartesiane del nodo nella forma (x,y) dentro un quadrato di dimensione edge_dim per lato
        Tree.nodes[node]['pos'] = (random.randint(0, edge_dim), random.randint(0, edge_dim))
        Tree.nodes[node]['chrg_station'] = False
        Tree.nodes[node]['color'] = 'grey'
    for (u, v) in Tree.edges():
        x1, y1 = Tree.nodes[u]['pos']
        x2, y2 = Tree.nodes[v]['pos']
        Tree.edges[u,v]['weight'] = get_distance((x1, y1), (x2, y2))
    return Tree

def get_random_flows(Tree: nx.Graph, K: int) -> list:
    flows = []
    for _ in range(K):
        nodes = list(Tree.nodes())
        node1 = random.choice(nodes)
        nodes.remove(node1)
        node2 = random.choice(nodes)
        flows.append([node1, node2])
    return flows

def get_random_chrg_stations(Tree: nx.Graph) -> list:
    """
    Function to get a list of random charging stations
    :param
        Tree: Tree to be analyzed
    :return
        chrg_stations: list of random charging stations
    """
    chrg_stations = []
    for node in Tree.nodes():
        if random.random() < 0.5:
            chrg_stations.append(node)
            Tree.nodes[node]['chrg_station'] = True
    return chrg_stations

def set_chrg_stations(Tree: nx.Graph, chrg_stations: list) -> None:
    """
    Function to set the charging stations
    :param
        Tree: Tree to be analyzed
        chrg_stations: list of charging stations
    """
    for node in Tree.nodes():
        if node in chrg_stations:
            Tree.nodes[node]['chrg_station'] = True
        

def __is_admissible(Tree: nx.Graph, flows: list, L: int) -> bool:
    """
    Function to check if the network is admissible
    :param
        Tree: Tree to be analyzed
        flows: list of flows
        L: battery capacity per vehicle
    :return
        True if the network is admissible, False otherwise
    """
    paths = get_all_paths_of_all_flows(Tree, flows)
    for path in paths:
        charge = L
        for i in range(len(path)-1):
            charge -= Tree.edges[path[i], path[i+1]]['weight']
            if Tree.nodes[path[i]]['chrg_station']:
                charge = L
            if charge < 0:
                return False
    return True

def get_weight_of_edges(Tree : nx.Graph):
    """
    Function to get a dictionary of all the edges with their associated weight
    :param
        Tree: Tree to be analyzed
    :return
        weight_of_edges: dictionary with the weight of the edges
    """
    weight_of_edges = {}
    for (u, v) in Tree.edges():
        weight_of_edges[(u,v)] = Tree.edges[u,v]['weight']
    return weight_of_edges


def draw_tree(Tree : nx.Graph):
    """
    Function to draw a tree using networkx
    :param 
        Tree: Tree to be drawn
    """
    colors = {'chrg_station':'green', 'no_chrg_station':'grey', 'o_k':'red', 'd_k':'yellow'}
    #pos = nx.spring_layout(Tree)
    for node in Tree.nodes():
        if Tree.nodes[node]['chrg_station']:
            Tree.nodes[node]['color'] = colors['chrg_station']
        else:
            Tree.nodes[node]['color'] = colors['no_chrg_station']
    nx.draw(
            Tree, 
            with_labels = True,
            node_color = [Tree.nodes[node]['color'] for node in Tree.nodes()],
            pos = nx.get_node_attributes(Tree, 'pos')
            )
    plt.show()


def get_distance(point1: (float, float), point2: (float, float)) -> float:
    """
    Function to get the distance between two points
    :param
        point1: first point
        point2: second point
    :return
        distance between the two points
    """
    return spatial.distance.euclidean(point1, point2)

def get_all_paths_of_all_flows(Tree: nx.Graph, flows: list) -> list:
    """
    Function to get all the paths of all the flows
    :param
        Tree: Tree to be analyzed
        flows: list of flows
    :return
        all_paths: list of all the paths of all the flows -> [[path1_flow1, path2_flow1, ...], [path1_flow2, path2_flow2, ...], ...]
    """
    paths = []
    for flow in flows:
        paths.append(nx.shortest_path(Tree, flow[0], flow[1]))
    return paths

