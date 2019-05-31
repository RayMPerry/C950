# Ray Perry - 000981059

import csv
from utils.graph import Node, Edge, Graph

def generate_graph():
    """
    Using these two pseudo-relational flat files, we're going to generate the graph needed for routing.
    """
    new_graph = Graph()
    
    with open("data/nodes.csv") as nodes_file:
        node_reader = csv.reader(nodes_file)
        for index, row in enumerate(node_reader):
            if index:
                new_graph.add_node(Node(row[0], row[1], row[2]));
                
    with open("data/distances.csv") as distances_file:
        distance_reader = csv.reader(distances_file)
        for index, row in enumerate(distance_reader):
            node_index = 0
            while node_index < index:
                node1 = new_graph.nodes[index]
                node2 = new_graph.nodes[node_index]
                new_graph.add_edge(Edge(node1, node2, row[node_index]))
                node_index += 1
                
    return new_graph

def start_app():
    """
    This is the main entrypoint for the program.
    """
    print('Generating routes.')
    graph = generate_graph()
    graph.show_edges(1)
    print('Beginning application.')


if __name__ == '__main__':
    start_app()
    
# Local Variables:
# compile-command: "python3 main.py"
# End:
