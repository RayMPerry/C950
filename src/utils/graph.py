class Node:
    number_of_nodes = 0
    
    def __init__(self, name, address, zip_code):
        self.id = self.__class__.number_of_nodes
        self.__class__.number_of_nodes += 1
        self.name = name.strip()
        self.address = address.strip()
        self.zip_code = zip_code.strip()
        self.edge_ids = []

    def display(self):
        print(f'Node #{self.id}: {self.name}, {self.address}, {self.zip_code}')

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

    def display(self):
        print(f'Edge: {self.distance} miles between nodes #{self.node_id_1} and #{self.node_id_2}.')
    
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
        def is_edge_selected(edge):
            return edge.get_edge_id() in self.edge_lookup[str(node_id)]
        
        selected_edges = [edge for edge in self.edges if is_edge_selected(edge)]
       
        for edge in selected_edges:
            edge.display()
