import networkx as nx
import matplotlib.pyplot as plt
from scipy import spatial
import random


def generate_random_network_tree(n_nodes: int, k_flow: int, edge_dim: int) -> nx.Graph:
    """
    Function to generate a random network tree with k flow
    :param 
        n_nodes: number of nodes in the tree
        k_flow: number of flow in the tree
        edge_dim: dimension of the edge of the square
    :return
        Tree: random network tree with k flow
    """
    Tree = nx.random_tree(n_nodes)
    for (u, v) in Tree.edges():
        Tree.edges[u,v]['weight'] = random.randint(1,10)

    return Tree

def get_weight_to_edges(Tree : nx.Graph):
    """
    Function to get the weight of the edges of the tree
    :param
        Tree: Tree to be analyzed
    :return
        weight_to_edges: dictionary with the weight of the edges
    """
    print("ciao")
    weight_to_edges = {}
    for (u, v) in Tree.edges():
        weight_to_edges[(u,v)] = Tree.edges[u,v]['weight']
    return weight_to_edges


def draw_tree(Tree : nx.Graph):
    """
    Function to draw a tree using networkx
    :param 
        Tree: Tree to be drawn
    """
    colors = {'colonnina':'green', 'no_colonnina':'grey', 'o_k':'red', 'd_k':'yellow'}
    #pos = nx.spring_layout(Tree)
    nx.draw(Tree, with_labels=True)
    plt.show()


def get_distance(point1, point2):
    """
    Function to get the distance between two points
    :param
        point1: first point
        point2: second point
    :return
        distance between the two points
    """
    return spatial.distance.euclidean(point1, point2)