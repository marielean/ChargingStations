import networkx as nx
import matplotlib.pyplot as plt
from scipy import spatial
import random, json
import numpy as np

def get_wight_of_neighbours_of_a_node(Tree: nx.Graph, node: str):
    '''
    Returns the weight of the edges connected to the node
    param:
        Tree: Tree to be analyzed
        node: node to be analyzed
    return:
        list of tuples (node, weight) -> [(node1, weight1), (node2, weight2), ...]
    '''
    node = str(node)
    return [(int(ng_node), Tree.edges[(node, ng_node)]['weight']) for ng_node in list(Tree.neighbors(node))]

def get_weight_of_nodes_edge_ordered(T: nx.Graph, flows: list, N: int, reverse: bool = True) -> any:
    '''
    Returns the weights of the nodes and the edges ordered in a list
    :param
        T: Tree to be analyzed
        flows: list of flows
        N: number of nodes
        reverse: if True, the list is ordered in descending order, otherwise in ascending order
    :return
        sorted_nodes_weights: list of weights of the nodes ordered
        sorted_nodes_index: list of indexes of the nodes ordered
    '''
    nodes_index = list(range(N))
    nodes_weights, _ = get_weights(T, flows)
    sorted_tuples = sorted(zip(nodes_weights, nodes_index), reverse=reverse)
    sorted_nodes_weights, sorted_nodes_index = zip(*sorted_tuples)
    sorted_nodes_weights = list(sorted_nodes_weights)
    sorted_nodes_index = list(sorted_nodes_index)
    

    return sorted_nodes_weights, sorted_nodes_index

def save_results(filename: str, results: list , mode: str = 'w') -> None:
    '''
    Function to save the results of the algorithm in a json file
    :param
        filename: name of the file to be saved
        results: list of results to be saved
        mode: mode to open the file
    '''
    results = [str(result) for result in results]
    with open('saved_data/'+filename+'.json', mode) as file:
        json.dump(results, file)

def load_results(filename: str) -> list:
    '''
    Return the results from a file 
    :param
        filename: name of the file to be loaded
    :return
        results: list of results loaded from the file
    '''
    with open('saved_data/'+filename+'.json', 'r') as file:
        results = json.load(file)
    
    results = [str(result) for result in results]
    return results

def get_weights(Tree: nx.Graph, flows: list):
    '''
    Returns:
        - the weights of the nodes calculated as the sum of how much each node is used by the flows
        - the weights of the paths of the flows calculated as the sum of the weights of the nodes in the path
    :param
        Tree: Tree to be analyzed
        flows: list of flows
    :return
        nodes_weights: list of weights of the nodes
        paths_weights: list of weights of the paths
    '''
    def get_nodes_weight(Tree: nx.Graph, flows: list):
        '''
        Returns the weights of the nodes calculated as the sum of how much each node is used by the flows
        '''
        paths = get_all_paths_of_all_flows(Tree, flows)
        nodes_weights = []
        for node in Tree.nodes:
            weight = 0
            for path in paths:
                if node in path:
                    weight += 1
            nodes_weights.append(weight)
        return nodes_weights

    def get_paths_weight(Tree: nx.Graph, flows: list):
        '''
        Returns the weights of the paths of the flows calculated as the sum of the weights of the nodes in the path
        '''
        paths = get_all_paths_of_all_flows(Tree, flows)
        paths_weight = []
        nodes_weight = get_nodes_weight(Tree, flows)
        for path in paths:
            weight = 0
            for node in path:
                weight += nodes_weight[int(node)]
            paths_weight.append(weight)
        return paths_weight
    
    return get_nodes_weight(Tree, flows), get_paths_weight(Tree, flows)

def generate_random_network_tree(N: int, K: int, L: int, edge_dim: int) -> nx.Graph:
    """
    Generates a random network tree with K flows
    :param 
        N: number of nodes in the tree network
        K: number of flows in the tree network
        L: battery capacity per vehicle
        edge_dim: dimension of the edge of the square where the network is located
    :return
        Tree: random network tree with k flows
    """
    Tree = nx.random_tree(N)

    # Generate random sources and destinations for each flow
    Tree.graph['N'] = N
    Tree.graph['K'] = K
    Tree.graph['L'] = L
    Tree.graph['edge_dim'] = edge_dim

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
    """
    Generates random flows in the tree network. The flows are generated by choosing random sources and destinations. The cost of the path of every flow is checked to be more than the battery capacity.
    :param 
        Tree: Tree to be analyzed
        K: number of flows
    :return
        flows: list of flows in the form [[source1, destination1], [source2, destination2], ...]
    """
    flows = []
    L = Tree.graph['L']
    for _ in range(K):
        nodes = list(Tree.nodes())
        node1 = random.choice(nodes)
        nodes.remove(node1)
        node2 = random.choice(nodes)
        path = nx.shortest_path(Tree, node1, node2)
        # verify if the cost of the path is less than the battery capacity
        while sum([Tree.edges[path[i], path[i+1]]['weight'] for i in range(len(path)-1)]) < L:
            nodes = list(Tree.nodes())
            node1 = random.choice(nodes)
            nodes.remove(node1)
            node2 = random.choice(nodes)
            path = nx.shortest_path(Tree, node1, node2)
        
        flows.append([str(node1), str(node2)])

        '''cost = sum([Tree.edges[path[i], path[i+1]]['weight'] for i in range(len(path)-1)])
        if cost > L:
            flows.append([str(node1), str(node2)])
        else:
            # if the cost is less than the battery capacity, there is no sense to add this specific flow to the list
            K = Tree.graph['K']
            Tree.graph['K'] = K - 1'''
    return flows

def save_tree(Tree: nx.Graph, flows: list, filename: str) -> None:
    """
    Saves the tree in a custom `.gml` file and the flows in a default `.json` file
    :param
        Tree: Tree to be saved
        filename: name of the file
    """
    nx.write_gml(Tree, filename)
    # Open a file in write mode
    with open('tree_net/flows.json', 'w') as file:
        json.dump(flows, file)

def load_all_data(filename: str) -> any:
    """
    Loads all necessary data from two files
    :param
        filename: name of the file
    :return
        Tree: Tree loaded from the file
        flows: list of flows
        L: battery capacity per vehicle
        K: number of flows
        N: number of nodes
    """
    Tree = nx.read_gml(filename)
    with open('tree_net/flows.json', 'r') as file:
        flows = json.load(file)
    return Tree, flows, Tree.graph['L'], Tree.graph['K'], Tree.graph['N']

def draw_tree(Tree : nx.Graph, flows: list):
    """
    Draws the given tree using networkx. Includes colors for charging stations, origins and destinations.
    :param 
        Tree: Tree to be drawn
        flows: list of flows in the form [[source1, destination1], [source2, destination2], ...]
    """

    colors = {'chrg_station':'green', 'o_k':'red', 'd_k':'yellow', 'od_k': 'orange', 'ch-od_k': 'blue'}
    
    for node in Tree.nodes():
        if Tree.nodes[node]['chrg_station'] and (str(node) in [flow[0] for flow in flows] or str(node) in [flow[1] for flow in flows]):
            Tree.nodes[node]['color'] = colors['ch-od_k']
        elif Tree.nodes[node]['chrg_station']:
            Tree.nodes[node]['color'] = colors['chrg_station']
        elif str(node) in [flow[0] for flow in flows]:
            if str(node) in [flow[1] for flow in flows]:
                Tree.nodes[node]['color'] = colors['od_k']
            else:
                Tree.nodes[node]['color'] = colors['o_k']
        elif str(node) in [flow[1] for flow in flows]:
            Tree.nodes[node]['color'] = colors['d_k']
    plt.figure(figsize=(15,15))
    nx.draw_networkx(
            Tree, 
            with_labels = True,
            node_color = [Tree.nodes[node]['color'] for node in Tree.nodes()],
            pos = nx.spring_layout(Tree, seed=42)
            )
    plt.show()

def get_all_paths_of_all_flows(Tree: nx.Graph, flows: list) -> list:
    """
    Returns a list of paths, one for each flow from source to destination.
    :param
        Tree: Tree to be analyzed
        flows: list of flows
    :return
        paths: list of paths (a path for each flow) -> [[path_flow1], [path_flow2], ...]
    """
    paths = []
    for flow in flows:
        paths.append(nx.shortest_path(Tree, flow[0], flow[1]))
    return paths

def get_chrg_stations_per_path(Tree: nx.Graph, path: list, L: int, charging_stations: set):
    '''
    Returns the set of charging stations for a specific path of a flow with the naive greedy algorithm.
    :param
        Tree: Tree to be analyzed
        path: path of a flow
        L: battery capacity per vehicle
        charging_stations: set of charging stations, initially empty
    :return
        charging_stations: set of charging stations for the specific path
    '''
    charge = L
    for i in range(len(path) - 1):
            charge -= Tree.edges[(path[i], path[i+1])]['weight']
            if charge < 0:
                charging_stations.add(path[i])
                Tree.nodes[path[i]]['chrg_station'] = True
                charge = L
                charge -= Tree.edges[(path[i], path[i+1])]['weight']
    return charging_stations

def get_chrg_stations_with_memory(Tree: nx.Graph, path: list, L: int, charging_stations: set):
    '''
    Returns the set of charging stations for a specific path of a flow with memory greedy algorithm.
    :param
        Tree: Tree to be analyzed
        path: path of a flow
        L: battery capacity per vehicle
        charging_stations: set of charging stations, initially empty
    :return
        charging_stations: set of charging stations for the specific path
    '''
    charge = L
    for i in range(len(path) - 1):
        if path[i] in charging_stations:
            charge = L
        charge -= Tree.edges[(path[i], path[i+1])]['weight']
        if charge < 0:
            charging_stations.add(path[i])
            Tree.nodes[path[i]]['chrg_station'] = True
            charge = L
            charge -= Tree.edges[(path[i], path[i+1])]['weight']
    return charging_stations

def set_chrg_stations(Tree: nx.Graph, chrg_stations: list[str]) -> None:
    """
    Sets the charging stations in the graph
    :param
        Tree: Tree with nodes to be set as charging stations
        chrg_stations: list of charging stations
    """
    chrg_stations =[str(element) for element in chrg_stations]
    for node in Tree.nodes():
        if node in chrg_stations:
            Tree.nodes[node]['chrg_station'] = True

def get_weight_of_edges(Tree : nx.Graph):
    """
    Returns a dictionary with the weight of the edges
    :param
        Tree: Tree to be analyzed
    :return
        weight_of_edges: dictionary with the weight of the edges
    """
    weight_of_edges = {}
    for (u, v) in Tree.edges():
        weight_of_edges[(u,v)] = Tree.edges[u,v]['weight']
    return weight_of_edges

def cont_chrg_stations(Tree: nx.Graph) -> int:
    """
    Returns the number of charging stations in the graph
    :param
        Tree: Tree to be analyzed
    :return
        count: number of charging stations
    """
    count = 0
    for node in Tree.nodes():
        if Tree.nodes[node]['chrg_station']:
            count += 1
    return count

def reset_chrg_stations(Tree: nx.Graph) -> None:
    '''
    Function to reset chrging stations in the graph
    :param
        Tree: Tree to be reseted
    '''
    for node in Tree.nodes():
        Tree.nodes[node]['chrg_station'] = False

def is_admissible_paths(Tree: nx.Graph, paths: list, L: int) -> bool:
    """
    Function to check if the solution is admissible
    :param
        Tree: Tree to be analyzed
        paths: list of paths of all flows
        L: battery capacity per vehicle
    :return
        True if the network is admissible, False otherwise
    """
    for path in paths:
        charge = L
        for i in range(len(path)-1):
            charge -= Tree.edges[path[i], path[i+1]]['weight']
            if Tree.nodes[path[i]]['chrg_station']:
                charge = L
                charge -= Tree.edges[path[i], path[i+1]]['weight']
            if charge < 0:
                return False
    return True  

def set_on_tree_random_chrg_stations(Tree: nx.Graph) -> list:
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
  
def is_admissible(Tree: nx.Graph, flows: list, L: int) -> bool:
    """
    Function to check if the solution is admissible
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
                # la modifica si trova qui
                charge -= Tree.edges[path[i], path[i+1]]['weight']
            if charge < 0:
                return False
    return True

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

def get_weights_matrix(T: nx.Graph, flows: list) -> (np.ndarray):
    '''
    Function to get the weights matrix of the graph and the weights of the flows and the nodes.
    Every row of the matrix is a flow, every column is a node. The value of the every cell is the number of how many times the flows are passed through the node.
    :param
        T: Tree to be analyzed
        flows: list of flows
        paths: list of paths of all flows
    :return
        weights: matrix of weights
        flows_weights: array of weights of the flows
        nodes_weights: array of weights of the nodes
    '''

    N = len(T.nodes)
    K = len(flows)
    paths = get_all_paths_of_all_flows(T, flows)
    weights = np.zeros((K, N), dtype=int)
    for k in range(K):
        for path in paths[k]:
            for node in path:
                weights[k][int(node)] += 1
    
    
    flows_weights = np.zeros(K, dtype=int)
    for k in range(K):
        # somma la riga prima riga della matrice dei pesi
        flows_weights[k] = np.sum(weights[k])
    
    
    nodes_weights = np.zeros(N, dtype=int)
    for n in range(N):
        # somma la prima colonna della matrice dei pesi
        nodes_weights[n] = np.sum(weights[:, n])
    
    return weights, flows_weights, nodes_weights