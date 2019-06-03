import csv

class Node:
    # This is my node class.
    number_of_nodes = 0
    
    def __init__(self, name, address, zip_code):
        # Set up.
        self.id = self.__class__.number_of_nodes
        self.__class__.number_of_nodes += 1
        self.name = name.strip()
        self.address = address.strip()
        self.zip_code = zip_code.strip()
        self.edge_ids = []

    def __str__(self):
        # Returns a formatted string describing the Node.
        return f'Node #{self.id}: {self.name}, {self.address}, {self.zip_code}'

class Edge:
    # This is my edge class.
    number_of_edges = 0
    
    def __init__(self, node1, node2, distance):
        # Set up.
        self.id = self.__class__.number_of_edges
        node1.edge_ids.append(self.id);
        node2.edge_ids.append(self.id);
        self.__class__.number_of_edges += 1
        
        self.node_id_1 = node1.id
        self.node_id_2 = node2.id
        self.distance = distance

    def __str__(self):
        # Returns a formatted string describing the Edge.
        return f'Edge: {self.distance} miles between nodes #{self.node_id_1} and #{self.node_id_2}.'

class Graph:
    # This is my graph class.
    def __init__(self):
        # Set up.
        self.nodes = []
        self.edges = []
        self.edge_lookup = {}

    def add_node(self, node):
        # This adds a node to the nodes list.
        self.nodes.append(node)

    def add_edge(self, edge):
        # This adds a edge to the edges list and to the edge lookup table.
        self.edges.append(edge)
        
        source = f'{edge.node_id_1}'
        destination = f'{edge.node_id_2}'
        
        if not source in self.edge_lookup:
            # If there isn't an entry for this source, make one.
            self.edge_lookup.update({ f'{source}': [] })
        self.edge_lookup[source].append(edge.id)

        if not destination in self.edge_lookup:
            # If there isn't an entry for this destination, make one.
            self.edge_lookup.update({ f'{destination}': [] })
        self.edge_lookup[destination].append(edge.id)

    def show_edges(self, node_id):
        # This shows us all the edges connected to a node.
        is_edge_selected = lambda edge: edge.id in self.edge_lookup[str(node_id)]
        return list(filter(is_edge_selected, self.edges))

    def get_node_by_address(self, address):
        # This gets a node by its address.
        is_node_selected = lambda node: node.address == address
        selected_nodes = list(filter(is_node_selected, self.nodes))
        return selected_nodes[0] if len(selected_nodes) > 0 else None

    def get_edge_by_addresses(self, address1, address2):
        # This gets the connecting edge between two addresses.
        node1 = self.get_node_by_address(address1)
        node2 = self.get_node_by_address(address2)
        selected_edge_id = set(self.edge_lookup[str(node1.id)]) & set(self.edge_lookup[str(node2.id)])
        if not len(selected_edge_id):
            return None
        return self.edges[selected_edge_id.pop()]

def generate():
    # Using these pseudo-relational flat files, we're going to generate the graph needed for routing.
    new_graph = Graph()
    
    with open("data/nodes.csv") as nodes_file:
        # Using this csv file...
        node_reader = csv.reader(nodes_file)
        for index, row in enumerate(node_reader):
            # Iterate over each row.
            if index:
                # Ignore the header.
                new_graph.add_node(Node(row[0], row[1], row[2]));
                
    with open("data/distances.csv") as distances_file:
        # Using this csv file...
        distance_reader = csv.reader(distances_file)
        for index, row in enumerate(distance_reader):
            # Iterate over each row.
            node_index = 0
            while node_index < index:
                # As long as the `node_index` is less than the actual `index`, we shouldn't add an edge for the same place.
                node1 = new_graph.nodes[index]
                node2 = new_graph.nodes[node_index]
                new_graph.add_edge(Edge(node1, node2, row[node_index]))
                node_index += 1
                
    return new_graph
