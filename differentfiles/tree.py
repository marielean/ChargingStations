import networkx as nx
import matplotlib.pyplot as plt
from scipy import spatial
import random



class Tree_net:
    """
    Class to generate a random network tree with k flow
    """
    def __init__(self) -> None:
        pass

    def generate_random_network_tree(self, n_nodes: int, k_flow: int, edge_dim: int) -> nx.Graph:
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
        self.Tree = Tree
        return Tree
    
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