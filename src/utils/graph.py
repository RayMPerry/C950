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

    def get_node_id(self):
        return self.id
    
    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_zip_code(self):
        return self.zip_code

    def get_edge_ids(self):
        return self.edge_ids

class Edge:
    number_of_edges = 0
    
    def __init__(self, node1, node2, distance):
        self.id = self.__class__.number_of_edges
        node1.edge_ids.append(self.id);
        node2.edge_ids.append(self.id);
        self.__class__.number_of_edges += 1
        
        self.node_id_1 = node1.get_node_id()
        self.node_id_2 = node2.get_node_id()
        self.distance = distance

    def __str__(self):
        return f'Edge: {self.distance} miles between nodes #{self.node_id_1} and #{self.node_id_2}.'
    
    def get_edge_id(self):
        return self.id
    
    def get_first_node_id(self):
        return self.node_id_1

    def get_second_node_id(self):
        return self.node_id_2

    def get_distance(self):
        return self.distance

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.edge_lookup = {}

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)
        
        source = f'{edge.get_first_node_id()}'
        destination = f'{edge.get_second_node_id()}'
        
        if not source in self.edge_lookup:
            self.edge_lookup.update({ f'{source}': [] })
        self.edge_lookup[source].append(edge.get_edge_id())

        if not destination in self.edge_lookup:
            self.edge_lookup.update({ f'{destination}': [] })
        self.edge_lookup[destination].append(edge.get_edge_id())

    def show_edges(self, node_id):
        is_edge_selected = lambda edge: edge.get_edge_id() in self.edge_lookup[str(node_id)]
        return list(filter(is_edge_selected, self.edges))

    def get_node_by_address(self, address):
        is_node_selected = lambda node: node.get_address() == address
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
