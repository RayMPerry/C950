import csv

class Node:
    number_of_nodes = 0
    
    def __init__(self, name, address, zip_code):
        self.id = self.__class__.number_of_nodes
        self.__class__.number_of_nodes += 1
        self.name = name.strip()
        self.address = address.strip()
        self.zip_code = zip_code.strip()
        self.edge_ids = []

    def __str__(self):
        return f'Node #{self.id}: {self.name}, {self.address}, {self.zip_code}'

class Edge:
    number_of_edges = 0
    
    def __init__(self, node1, node2, distance):
        self.id = self.__class__.number_of_edges
        node1.edge_ids.append(self.id);
        node2.edge_ids.append(self.id);
        self.__class__.number_of_edges += 1
        
        self.node_id_1 = node1.id
        self.node_id_2 = node2.id
        self.distance = distance

    def __str__(self):
        return f'Edge: {self.distance} miles between nodes #{self.node_id_1} and #{self.node_id_2}.'

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.edge_lookup = {}

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)
        
        source = f'{edge.node_id_1}'
        destination = f'{edge.node_id_2}'
        
        if not source in self.edge_lookup:
            self.edge_lookup.update({ f'{source}': [] })
        self.edge_lookup[source].append(edge.id)

        if not destination in self.edge_lookup:
            self.edge_lookup.update({ f'{destination}': [] })
        self.edge_lookup[destination].append(edge.id)

    def show_edges(self, node_id):
        is_edge_selected = lambda edge: edge.id in self.edge_lookup[str(node_id)]
        return list(filter(is_edge_selected, self.edges))

    def get_node_by_address(self, address):
        is_node_selected = lambda node: node.address == address
        selected_nodes = list(filter(is_node_selected, self.nodes))
        return selected_nodes[0] if len(selected_nodes) > 0 else None

    def get_node_by_zip_code(self, zip_code):
        pass


def generate():
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
