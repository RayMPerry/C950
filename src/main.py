# Ray Perry - 000981059

import utils.graph as graph

def start_app():
    """
    This is the main entrypoint for the program.
    """
    print('Generating routes.')
    route_graph = graph.generate()
    node = route_graph.get_node_by_address('3575 W Valley Central Station Bus Loop')
    print(route_graph.show_edges(node.get_node_id()))
    print('Beginning application.')


if __name__ == '__main__':
    start_app()
    
# Local Variables:
# compile-command: "python3 main.py"
# End:
