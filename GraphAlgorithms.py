from GraphStructure import Graph, Node, Edge, DummyLogicalEdge


class MergeSort:
    """The Merge Sort is called by several algorithms at different parts since it is the most efficient way - it's
    used for sorting edges of priority queues by their weight into ascending order. It efficiently carries out the sort
    using recursion by:
    - Dividing the list into two sublists and repeating this on each sublist until each item has been separated
    - Merging two sublists into one sorted list and repeating this on sublists until whole list has been merged"""

    def __init__(self, edges):
        self.edges = edges

    def edges_mergesort_ascending(self):
        self.edges = self._merge_sort_ascending(self.edges)
        return self.edges

    def _merge_sort_ascending(self, edges):
        """The sorting function of the algorithm which divides the list and then merges them sorted"""
        if len(edges) <= 1: # No need to sort if only one item
            return edges
        # Divide lists into two sublists
        middle = len(edges) // 2
        left_half = self._merge_sort_ascending(edges[:middle])
        right_half = self._merge_sort_ascending(edges[middle:])
        return self._merge_ascending(left_half, right_half) # Calls 'merge' method to merge them sorted

    def _merge_ascending(self, left, right):
        """Merges two sorted lists into one sorted list in ascending order"""
        sorted_edges = []
        sublist1_index = 0
        sublist2_index = 0
        # Traversing through both list, adding  the lower weighted edge to the sorted list then moving onto the next
        while sublist1_index < len(left) and sublist2_index < len(right):
            if left[sublist1_index].weight <= right[sublist2_index].weight:
                sorted_edges.append(left[sublist1_index])
                sublist1_index += 1
            else:
                sorted_edges.append(right[sublist2_index])
                sublist2_index += 1
        # Adding remaining edges to sorted list
        sorted_edges.extend(left[sublist1_index:])
        sorted_edges.extend(right[sublist2_index:])
        return sorted_edges


class NearestNeighbour:
    def __init__(self, input_graph):
        self.input_graph = input_graph
        self.output_path = Graph()

    def find_path(self, starting_node):
        self.output_path.add_node(starting_node)
        visited_nodes = []
        output_path_edges = []

        current_node = starting_node
        visited_nodes.append(starting_node)

        while len(self.output_path.nodes) < len(self.input_graph.nodes):
            connected_edges_queue = list(current_node.edges)
            edge_sorter = MergeSort(connected_edges_queue)
            connected_edges_queue = edge_sorter.edges_mergesort_ascending() # Edges connected to current node

            new_edge = None
            # Traversing through current node's edges to add lowest weight connecting to unvisited
            for edge in connected_edges_queue:
                for node in edge.nodes:
                    if node != current_node and node not in visited_nodes:
                        new_edge = edge
                if new_edge:
                    break
            # Updating current node
            for node in new_edge.nodes:
                if node != current_node:
                    new_node = node

            # Updating output path
            self.output_path.add_node(new_node)
            self.output_path.add_edge(new_edge)
            visited_nodes.append(new_node)
            output_path_edges.append(new_edge)
            current_node = new_node

        log = []
        log.append("Starting Node: " + starting_node.label)
        log.append("")

        path_orderednodes_labels = []
        for node in visited_nodes:
            path_orderednodes_labels.append(node.label)
        path_str = "──".join(path_orderednodes_labels)  # Edge labels separated by commas
        log.append("Nearest Neighbour Path: " + path_str)

        path_edges_labels = []
        for edge in self.output_path.edges:
            path_edges_labels.append(edge.edge_label)
        path_edges_calc_str = " + ".join(path_edges_labels)  # Edge labels separated by commas
        log.append("Total Path Weight = " + path_edges_calc_str + " = " + str(self.output_path.total_weight))
        log.append("Total Weight: " + str(self.output_path.total_weight))
        self.output_path.log = log

        return self.output_path


class PrimsMST:
    """This class is used to process the inputted graph by the user and carry out Prim's algorithm, returning the
    output MST. The MST is constructed and returned with steps through the find_MST method."""

    def __init__(self, input_graph):
        self.input_graph = input_graph
        self.MST_output = Graph()

    def find_MST(self, starting_node):
        """The method used by Prim algorithm to construct the MST in summary is:
        Add the lowest weight edge that connects a node already in the tree to a node not yet in the tree.
        Repeating this process eventually constructs the MST once all nodes have been added to the graph

        In implementing the algorithm, the following components have been used:
        - A 'visited_nodes' set to track the nodes already added to the tree (which is used in identifying those edges
        that connect a node already in the tree to a node not yet in the tree)
        - A 'connected_edges_queue' which is a priority queue used to stores the edges that are connected to the
         visited nodes in the tree. Whenever a new node is added, the connected edges queue is updated accordingly.
         Each time, the queue is first sorted into ascending order by weight by calling the Merge Sort."""

        self.MST_output.add_node(starting_node) # Adding the inputted starting node to the MST to begin
        visited_nodes = set() # Set for tracking visited nodes
        visited_nodes.add(starting_node)
        connected_edges_queue = list(starting_node.edges) # Priority queue for the connected edges to tree being built
        MST_edges = [] # Stores the edges of the MST being built

        # Repeating the Prim's algorithm steps until all the input graph's nodes have been added to the MST
        while len(self.MST_output.nodes) < len(self.input_graph.nodes) and connected_edges_queue:
            # Sorting priority queue of connected edges by calling merge sort (ascending by weight)
            edge_sorter = MergeSort(connected_edges_queue)
            connected_edges_queue = edge_sorter.edges_mergesort_ascending()

            # Dequeuing from the priority queue to retrieve lowest weight connected edge to the current tree
            new_edge = connected_edges_queue.pop(0)
            new_node = None
            # Identifying the new node that the edge connects (or if it doesn't)
            if new_edge.node1 not in visited_nodes:
                new_node = new_edge.node1
            elif new_edge.node2 not in visited_nodes:
                new_node = new_edge.node2

            # Adding edge to the MST if it connects a new node (to one already in the tree graph being built)
            if new_node:
                self.MST_output.add_node(new_node)
                self.MST_output.add_edge(new_edge)
                MST_edges.append(new_edge)
                visited_nodes.add(new_node) # Adding new node to the visited nodes

                # Updating the connected edges priority queue by adding the new edges connected to the new node
                for edge in new_node.edges:
                    if edge.node1 not in visited_nodes or edge.node2 not in visited_nodes:
                        connected_edges_queue.append(edge)

        # Storing steps as strings in the log and assigning to outputted MST
        log = []
        log.append("Starting Node: " + starting_node.label)
        log.append("")
        MST_edges_labels = []
        for edge in self.MST_output.edges:
            MST_edges_labels.append(edge.edge_label)
        MST_edges_str = ", ".join(MST_edges_labels)  # Edge labels separated by commas
        log.append("MST Edges (In Order of Selection): " + MST_edges_str)
        log.append("Total MST Weight: " + str(self.MST_output.total_weight))
        self.MST_output.log = log  # Assigning built log to the MST output graph

        return self.MST_output


class KruskalsMST:
    """This class is used to process the inputted graph by the user and carry out the Kruskal's algorithm, returning
    the output MST. The MST is constructed and returned with steps through the find_MST method. To begin, the
    output MST is initialised with copies of the input graph's nodes so it can be used for testing when constructing
    the MST."""

    def __init__(self, input_graph):
        self.input_graph = input_graph
        self.MST_output = Graph()

        # Taking copies of inputted graph's nodes to test tentatively on the output MST
        self.copied_nodes = {} # Dictionary to map input graph nodes to cloned nodes
        for node in self.input_graph.nodes:
            node_copy = Node(node.label, node.scenePos().x(), node.scenePos().y())
            self.MST_output.add_node(node_copy)
            self.copied_nodes[node] = node_copy

    def find_MST(self):
        """The MST is constructed by:
        - Sorting the edges by weight into ascending order within a priority queue (by calling the merge sort)
        - Traversing through the priority queue and adding edges tentatively to the output MST to check if they create
        a cycle - adding it to the MST if they don't, discarding the edge if it does. The testing for cycles utilises
        a depth-first-search which involves recursion

        The output MST is returned and the logs of the steps followed are stored to display to the user including steps:
        - The edge sorting into ascending order
        - The accepting and rejecting of edges
        - The final MST's edges and its total weight"""

        log = [] # Stores required steps followed in log to display to user

        # Sorting edges into ascending order
        edge_sorter = MergeSort(self.input_graph.edges)
        sorted_edges_queue = edge_sorter.edges_mergesort_ascending() # Priority queue for edges by ascending weight
        # Storing line for edge sorting as a string in the log
        sorted_edges_labels = []
        for edge in sorted_edges_queue:
            sorted_edges_labels.append(edge.edge_label)
        sorted_edges_str = ", ".join(sorted_edges_labels) # Edge labels seperated by commas
        log.append("Sorted Edges (Ascending): " + sorted_edges_str)
        log.append("")

        # Traversing through edges priority queue and testing if adding the edge creates a cycle
        while len(self.MST_output.edges) < (len(self.MST_output.nodes) - 1) and sorted_edges_queue:
            smallest_edge = sorted_edges_queue.pop(0)
            edge_node1 = self.copied_nodes[smallest_edge.node1]
            edge_node2 = self.copied_nodes[smallest_edge.node2]
            # Creating a dummy logical edge to tentatively add to the MST output
            test_edge = DummyLogicalEdge(smallest_edge.weight, edge_node1, edge_node2)
            self.MST_output.edges.append(test_edge)
            # Checking if adding the edge created a cycle and accordingly adding it to the MST or discarding it
            if self._check_cycles(self.MST_output) == True:
                self.MST_output.edges.remove(test_edge)
                log.append("Reject " + smallest_edge.edge_label) # Storing edge rejection step to log
            else:
                self.MST_output.edges.remove(test_edge)
                log.append("Accept " + smallest_edge.edge_label) # Storing edge acceptance step to log
                real_edge = Edge(smallest_edge.weight, edge_node1, edge_node2, None)
                self.MST_output.add_edge(real_edge)
        log.append("")

        # Storing final steps as strings in the log and assigning it to the constructed MST
        MST_edges_labels = []
        for edge in self.MST_output.edges:
            MST_edges_labels.append(edge.edge_label)
        MST_edges_str = ", ".join(MST_edges_labels)  # Edge labels separated by commas
        log.append("MST Edges: " + MST_edges_str)
        log.append("Total MST Weight: " + str(self.MST_output.total_weight))
        self.MST_output.log = log # Assigning built log to the MST output graph

        return self.MST_output

    def _check_cycles(self, graph):
        """Private method used in the class to check if adding an edge has created a cycle. A depth-first-search is
        used to carry this out, which recursively calls itself to traverse through the graph's nodes - if the
        depth-first-search returns to a visited node that's not the parent, it means there is a cycle. The method
        returns True if a cycle has been found and False if there is no cycle."""

        visited = set() # Stores visited nodes during the cycles check

        def depth_first_search(node, parent):
            visited.add(node) # Add current node to visited

            # Traversing through the neighbouring nodes connected to the current node
            for edge in graph.edges:

                # Locating neighbour node objects
                if edge.node1 is node:
                    neighbour = edge.node2
                elif edge.node2 is node:
                    neighbour = edge.node1
                else:
                    continue

                # Testing recursively for cycles
                if neighbour not in visited:
                    # Recursively call depth-first-search again to now test the neighbouring node
                    if depth_first_search(neighbour, node):
                        return True  # A cycle was found in the series of recursive calls
                elif neighbour != parent:
                    return True  # If neighbour is already visited but not the parent - means there's a cycle

            return False  # For no cycle found

        # Testing each part of the graph sequentially
        for node in graph.nodes:
            if node not in visited:
                # Testing for cycle on this part of the graph recursively through the depth-first-search
                if depth_first_search(node, None):
                    return True
        return False


class DijkstrasShortestPath:
    """This class is used to process the inputted graph by the user and carry out Dijkstra's algorithm, returning the
    shortest path between the inputted start and end node. The path is calculated and returned with steps through
    the find_shortest_path method. Dictionaries are initialised with node labels as keys for storing the Dijkstra's
    tables to display in working log."""

    def __init__(self, input_graph):
        self.input_graph = input_graph

        self.predecessors = {} # Dictionary to track preceding nodes in the shortest path
        self.visited_order = [] # Tracking order of nodes visited
        self.shortest_path = [] # Storing final shortest path solution

        # Dictionaries with node labels as keys for the Dijkstra's tables (to display in working log)
        self.labelling_orders = {}
        self.working_values_lists = {}
        self.current_working_values = {}
        self.final_labels = {}
        for node in self.input_graph.nodes:
            self.current_working_values[node.label] = float('inf') # Storing distances as infinity initially
            self.labelling_orders[node.label] = None
            self.final_labels[node.label] = None
            self.predecessors[node.label] = None
            self.working_values_lists[node.label] = []

    def find_shortest_path(self, start_node, end_node):
        """Finds the shortest path between the start and end node using Dijkstra's algorithm. The algorithm involves:
        - Updating working values of all neighbouring nodes to the node last given its final value (starting from the
        start node)
        - A working value is only replaced if the tentative value is lower than the current working value
        - A node's final value is given when it has the lowest working value from all the nodes without final values
        - Once all nodes are visited, final values are used to calculate the shortest path by tracing back from end to
        start node (via the predecessors dictionary)"""

        # Initialising values for starting node
        self.current_working_values[start_node.label] = 0
        self.working_values_lists[start_node.label].append(0)
        self.labelling_orders[start_node.label] = 1

        # Creating a set for unvisited nodes
        unvisited = set()
        for node in self.input_graph.nodes:
            unvisited.add(node.label)
        label_order = 2

        # Iterating the algorithm's steps until all the nodes have been visited
        while unvisited:
            # Finding the unvisited node with the smallest current working distance from the start node
            lowest_value = float('inf')
            current_label = None
            for label in unvisited:
                if self.current_working_values[label] < lowest_value:
                    lowest_value = self.current_working_values[label]
                    current_label = label
            if self.current_working_values[current_label] == float('inf'):
                break
            # Updating the values of the node found and marking it as visited
            unvisited.remove(current_label)
            self.visited_order.append(current_label)
            if self.labelling_orders[current_label] is None:
                self.labelling_orders[current_label] = label_order
                label_order += 1

            # Updating neighbouring nodes and their working values according to the new node marked
            for neighbor_label, weight in self.input_graph.distance_matrix[current_label].items():
                if weight > 0 and neighbor_label in unvisited:
                    tentative = self.current_working_values[current_label] + weight # Calculating new tentative value

                    # Replacing a neighbour's working value if tentative is lower than the current and updating logs
                    if tentative < self.current_working_values[neighbor_label]:
                        self.current_working_values[neighbor_label] = tentative
                        self.working_values_lists[neighbor_label].append(tentative)
                        self.predecessors[neighbor_label] = current_label # Tracking predecessor path


        self.final_labels = self.current_working_values.copy() # Marking final labels as final working values

        # Error handling for if the start node and end node have no path
        if self.current_working_values[end_node.label] == float('inf'):
            self.shortest_path = []
            total_weight = float('inf')
        # Recording the shortest path based on the filled final values (tracing back from end to start via predecessors)
        else:
            path = []
            current = end_node.label
            while current is not None:
                path.append(current)
                current = self.predecessors[current]
            self.shortest_path = path[::-1]
            total_weight = self.final_labels[end_node.label]

        return self.shortest_path, total_weight, self.labelling_orders, self.final_labels, self.working_values_lists


