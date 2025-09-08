from PyQt5.QtWidgets import (QMainWindow, QWidget, QSplitter, QGraphicsScene, QLineEdit, QTableWidgetItem,
                             QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QMessageBox, QLabel)
from PyQt5.QtGui  import QPainter, QFont
from PyQt5.QtCore import Qt

from GraphStructure import Graph, Node, Edge
from GraphAlgorithms import KruskalsMST, PrimsMST, DijkstrasShortestPath, NearestNeighbour
from Graphs_View import GraphView
from Graphs_AlgorithmSolutionWindows import MSTWindow, DijkstrasWindow


class GraphAlgorithmsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.graph = Graph()
        self.setWindowTitle("Graph Algorithms")
        self.setGeometry(100, 100, 1200, 800)

        # Customising styles
        app_font = QFont('Comic Sans', 20)
        self.setFont(app_font)
        self.setStyleSheet("""
            QWidget {
                font-family: 'Comic Sans', Arial, sans-serif;
                font-size: 25px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 25px;
                font-weight: bold;
                border-radius: 25px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-family: Arial, sans-serif;
                font-size: 30px;
            }
        """)

        # Create splitter between control panel and graph canvas
        splitter = QSplitter(Qt.Horizontal)

        # Canvas area for the graph
        self.scene = QGraphicsScene(self)
        self.view = GraphView(self.scene, self)
        self.view.setRenderHint(QPainter.Antialiasing)

        # Control Panel
        control_panel = QWidget()
        control_layout = QVBoxLayout()
        space_between_sections = 40
        space_between_parallel = 15
        space_between_buttons = 7

        # Graph Construction Controls:
        # Graph Construction title label
        graph_construction_label = QLabel("Graph Construction:")
        graph_construction_label.setAlignment(Qt.AlignLeft)
        control_layout.addWidget(graph_construction_label)

        # Node Controls:
        nodes_panel_layout = QHBoxLayout()

        # Add Node widgets
        add_nodes_layout = QVBoxLayout()
        self.addnode_label_input = QLineEdit()
        self.addnode_label_input.setPlaceholderText("Enter Node Label")
        self.add_node_button = QPushButton("Add Node")
        self.add_node_button.clicked.connect(self.add_node)

        add_nodes_layout.addWidget(self.addnode_label_input)
        add_nodes_layout.addWidget(self.add_node_button)

        # Delete Node widgets
        delete_nodes_layout = QVBoxLayout()
        self.deletenode_label_input = QLineEdit()
        self.deletenode_label_input.setPlaceholderText("Enter Node Label")
        self.delete_node_button = QPushButton("Delete Node")
        self.delete_node_button.clicked.connect(self.delete_node)

        delete_nodes_layout.addWidget(self.deletenode_label_input)
        delete_nodes_layout.addWidget(self.delete_node_button)

        # Adding both node widget sections parallel to each other
        nodes_panel_layout.addLayout(add_nodes_layout)
        nodes_panel_layout.addSpacing(space_between_parallel)
        nodes_panel_layout.addLayout(delete_nodes_layout)
        # Adding the nodes panel layout to the control panel
        control_layout.addLayout(nodes_panel_layout)
        control_layout.addSpacing(space_between_buttons)


        # Edge Controls:
        edges_panel_layout = QHBoxLayout()

        # Add Edge widgets
        add_edges_layout = QVBoxLayout()
        self.addedge_startnode_input = QLineEdit()
        self.addedge_startnode_input.setPlaceholderText("Start Node Label")
        self.addedge_endnode_input = QLineEdit()
        self.addedge_endnode_input.setPlaceholderText("End Node Label")
        self.addedge_weight_input = QLineEdit()
        self.addedge_weight_input.setPlaceholderText("Edge Weight")
        self.add_edge_button = QPushButton("Add Edge")
        self.add_edge_button.clicked.connect(self.add_edge)

        add_edges_layout.addWidget(self.addedge_startnode_input)
        add_edges_layout.addWidget(self.addedge_endnode_input)
        add_edges_layout.addWidget(self.addedge_weight_input)
        add_edges_layout.addWidget(self.add_edge_button)

        # Delete Edge widgets
        delete_edges_layout = QVBoxLayout()
        self.deleteedge_startnode_input = QLineEdit()
        self.deleteedge_startnode_input.setPlaceholderText("Start Node Label")
        self.deleteedge_endnode_input = QLineEdit()
        self.deleteedge_endnode_input.setPlaceholderText("End Node Label")
        self.delete_edge_button = QPushButton("Delete Edge")
        self.delete_edge_button.clicked.connect(self.delete_edge)

        delete_edges_layout.addWidget(self.deleteedge_startnode_input)
        delete_edges_layout.addWidget(self.deleteedge_endnode_input)
        delete_edges_layout.addWidget(self.delete_edge_button)

        # Adding both edge widget sections parallel to each other
        edges_panel_layout.addLayout(add_edges_layout)
        edges_panel_layout.addSpacing(space_between_parallel)
        edges_panel_layout.addLayout(delete_edges_layout)
        # Adding the edges panel layout to the control panel
        control_layout.addLayout(edges_panel_layout)
        control_layout.addSpacing(space_between_buttons)

        # Clear Graph Button
        self.clear_graph_button = QPushButton("Clear Graph")
        self.clear_graph_button.setStyleSheet(
            "background-color: #F44336; color: white; font-weight: bold; border-radius: 15px;")
        self.clear_graph_button.clicked.connect(self.clear_graph)
        control_layout.addWidget(self.clear_graph_button)
        control_layout.addSpacing(space_between_sections)


        # Algorithm Buttons & Controls:
        # Graph Algorithms title label
        graph_algorithms_label = QLabel("Graph Algorithms:")
        graph_algorithms_label.setAlignment(Qt.AlignLeft)
        control_layout.addWidget(graph_algorithms_label)

        # Nearest Neighbour
        nearest_neighbour_layout = QHBoxLayout()
        self.nearest_neighbour_start_node_input = QLineEdit()
        self.nearest_neighbour_start_node_input.setPlaceholderText("Starting Node")
        nearest_neighbour_layout.addWidget(self.nearest_neighbour_start_node_input, 1)
        nearest_neighbour_layout.addSpacing(space_between_parallel)

        self.nearest_neighbour_button = QPushButton("Nearest Neighbour")
        self.nearest_neighbour_button.setStyleSheet(
            "background-color: #2196F3; color: white; font-weight: bold; border-radius: 15px;")
        self.nearest_neighbour_button.clicked.connect(self.show_nearest_neighbour_path)
        nearest_neighbour_layout.addWidget(self.nearest_neighbour_button, 1)

        # Prim's MST
        prim_layout = QHBoxLayout()
        self.prim_start_node_input = QLineEdit()
        self.prim_start_node_input.setPlaceholderText("Starting Node")
        prim_layout.addWidget(self.prim_start_node_input, 1)
        prim_layout.addSpacing(space_between_parallel)

        self.prim_button = QPushButton("Prim's MST")
        self.prim_button.setStyleSheet(
            "background-color: #2196F3; color: white; font-weight: bold; border-radius: 15px;")
        self.prim_button.clicked.connect(self.show_prims_MST)
        prim_layout.addWidget(self.prim_button, 1)

        # Kruskal's MST
        self.kruskal_button = QPushButton("Kruskal's MST")
        self.kruskal_button.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; border-radius: 15px;")
        self.kruskal_button.clicked.connect(self.show_kruskals_MST)

        # Dijkstra's Shortest Path
        dijkstra_input_layout = QHBoxLayout()
        self.dijkstra_start_node_input = QLineEdit()
        self.dijkstra_start_node_input.setPlaceholderText("Start Node")
        self.dijkstra_end_node_input = QLineEdit()
        self.dijkstra_end_node_input.setPlaceholderText("End Node")
        dijkstra_input_layout.addWidget(self.dijkstra_start_node_input)
        dijkstra_input_layout.addSpacing(space_between_parallel)
        dijkstra_input_layout.addWidget(self.dijkstra_end_node_input)
        self.dijkstra_button = QPushButton("Dijkstra's Shortest Path")
        self.dijkstra_button.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; border-radius: 15px;")
        self.dijkstra_button.clicked.connect(self.show_dijkstra_shortest_path)

        # Adding algorithm buttons & controls to algorithms layout
        algorithms_layout = QVBoxLayout()
        algorithms_layout.addLayout(nearest_neighbour_layout)
        algorithms_layout.addSpacing(space_between_buttons)
        algorithms_layout.addLayout(prim_layout)
        algorithms_layout.addSpacing(space_between_buttons)
        algorithms_layout.addWidget(self.kruskal_button)
        algorithms_layout.addSpacing(space_between_buttons)
        algorithms_layout.addLayout(dijkstra_input_layout)
        algorithms_layout.addWidget(self.dijkstra_button)

        # Adding algorithms layout to control layout
        control_layout.addLayout(algorithms_layout)
        control_layout.addSpacing(space_between_sections)


        # Distance Matrix Display:
        self.matrix_table = QTableWidget()
        control_layout.addWidget(self.matrix_table)
        control_panel.setLayout(control_layout)
        splitter.addWidget(self.view)
        splitter.addWidget(control_panel)
        splitter.setSizes([800, 400])
        self.setCentralWidget(splitter)


    def add_node(self):
        # Storing label input (capitalising automatically)
        label = self.addnode_label_input.text().upper().strip()

        # Error message if label input is not a single letter
        if len(label) != 1 or not label.isalpha():
            QMessageBox.warning(self, "Input Error", "Node label must be a single letter!")
            return
        # Error message if node already exists
        for node in self.graph.nodes:
            if node.label == label:
                QMessageBox.warning(self, "Input Error", "Node cannot already exist!")
                return

        # Adding node to scene and logical graph, then updating matrix display
        x, y = 0, 0
        new_node = Node(label, x, y)
        self.scene.addItem(new_node)
        self.graph.add_node(new_node)
        self.update_matrix()

    def delete_node(self):
        # Storing label input (capitalising automatically)
        label = self.deletenode_label_input.text().upper().strip()

        # Error message if label input is not a single letter
        if len(label) != 1 or not label.isalpha():
            QMessageBox.warning(self, "Input Error", "Node label must be a single letter!")
            return
        # Searching for node to delete
        found = False
        for node in self.graph.nodes:
            if node.label == label:
                found = True
                node_to_remove = node
        # Error message if node doesn't exist
        if not found:
            QMessageBox.warning(self, "Input Error", "Node must already exist!")
            return

        # Deleting node from logical graph
        node_to_remove_edges = node_to_remove.edges[:]
        self.graph.delete_node(node_to_remove)
        # Deleting the node's connected edges from scene
        for edge in node_to_remove_edges:
            self.scene.removeItem(edge.weight_text)
            self.scene.removeItem(edge)
        # Deleting node from scene and updating matrix display
        self.scene.removeItem(node_to_remove)
        self.update_matrix()

    def add_edge(self):
        # Taking input for edge node's start & end label
        start_label = self.addedge_startnode_input.text().upper().strip()
        end_label = self.addedge_endnode_input.text().upper().strip()

        try:
            weight = int(self.addedge_weight_input.text().strip())
        # Error message if inputted edge weight is not integer
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Edge weight must be an integer!")
            return
        # Error message if inputted edge weight is not positive
        if weight <= 0:
            QMessageBox.warning(self, "Input Error", "Edge weight must be positive!")
            return
        # Error message if label inputs are not a single letter
        if len(start_label) != 1 or not start_label.isalpha() or len(end_label) != 1 or not end_label.isalpha():
            QMessageBox.warning(self, "Input Error", "Node labels must be a single letter!")
            return
        # Error message if inputted start node and end node is same
        if start_label == end_label:
            QMessageBox.warning(self, "Input Error", "Edge must be between two different nodes!")
            return

        # Locating the start and end nodes
        start_node = None
        for node in self.graph.nodes:
            if node.label == start_label:
                start_node = node
                break
        end_node = None
        for node in self.graph.nodes:
            if node.label == end_label:
                end_node = node
                break
        # Error messages if either of the inputted nodes aren't found
        if not start_node or not end_node:
            QMessageBox.warning(self, "Input Error", "Both nodes must exist!")
            return

        # Error message if edge already exists
        for edge in self.graph.edges:
            if edge.node1.label == start_label and edge.node2.label == end_label:
                QMessageBox.warning(self, "Input Error", "Edge cannot already exist!")
                return
            elif edge.node2.label == start_label and edge.node1.label == end_label:
                QMessageBox.warning(self, "Input Error", "Edge cannot already exist!")
                return

        # Adding the edge to the scene and logical graph then updating matrix display
        new_edge = Edge(weight, start_node, end_node, self.scene)
        self.scene.addItem(new_edge)
        self.graph.add_edge(new_edge)
        self.update_matrix()

    def delete_edge(self):
        # Taking input for edge node's start & end label
        start_label = self.deleteedge_startnode_input.text().upper().strip()
        end_label = self.deleteedge_endnode_input.text().upper().strip()

        # Error message if label inputs are not a single letter
        if len(start_label) != 1 or not start_label.isalpha() or len(end_label) != 1 or not end_label.isalpha():
            QMessageBox.warning(self, "Input Error", "Node labels must be a single letter!")
            return
        # Error message if inputted start node and end node is same
        if start_label == end_label:
            QMessageBox.warning(self, "Input Error", "Edge must be between two different nodes!")
            return

        # Locating the edge
        edge_to_remove = None
        for edge in self.graph.edges:
            if edge.node1.label == start_label and edge.node2.label == end_label:
                edge_to_remove = edge
                break
        if not edge_to_remove:
            for edge in self.graph.edges:
                if edge.node2.label == start_label and edge.node1.label == end_label:
                    edge_to_remove = edge
                    break

        # Error message if the edge is not found
        if not edge_to_remove:
            QMessageBox.warning(self, "Input Error", "Edge must already exist!")
            return

        # Deleting the edge from the scene and logical graph then updating matrix display
        self.graph.delete_edge(edge_to_remove)
        self.scene.removeItem(edge_to_remove.weight_text)
        self.scene.removeItem(edge_to_remove)
        self.update_matrix()

    def clear_graph(self):
        # Deleting all edges
        for edge in list(self.graph.edges):
            self.graph.delete_edge(edge)
            self.scene.removeItem(edge.weight_text)
            self.scene.removeItem(edge)
        # Deleting all nodes
        for node in list(self.graph.nodes):
            self.graph.delete_node(node)
            self.scene.removeItem(node)
        # Updating the matrix
        self.update_matrix()


    def update_matrix(self):
        # Defining display styles
        row_height = 50
        column_width = 80
        items_font = QFont("Comic Sans", 20)

        # Constructing empty matrix
        nodes = self.graph.nodes
        size = len(nodes)

        self.matrix_table.setRowCount(size)
        self.matrix_table.setColumnCount(size)
        self.matrix_table.clearContents()
        self.matrix_table.verticalHeader().setFixedWidth(column_width)
        self.matrix_table.horizontalHeader().setMinimumHeight(row_height)
        self.matrix_table.setHorizontalHeaderLabels([node.label for node in nodes])
        self.matrix_table.setVerticalHeaderLabels([node.label for node in nodes])
        self.matrix_table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.matrix_table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)

        # Setting Styles
        self.matrix_table.setStyleSheet("""
            QTableWidget {
                gridline-color: black;
                background-color: white;
                border: none;
            }
            QTableWidget::item {
                border: 1px solid black;
                background-color: white;
            }
            QHeaderView::section {
                font-family: 'Comic Sans';
                font-size: 30px;
                border: 1.5px solid black;
                background-color: white;
                padding: 0px;
                margin: 0px;
            }
            QHeaderView {
                border: none;
                background-color: white;
            }
            QTableCornerButton::section {
                background-color: white;
                border: 1.5px solid black;
                margin: 0px;
                padding: 0px;
            }
        """)

        # Filling in matrix (retrieving data from logical graph's nested dictionary matrix)
        for i, node1 in enumerate(nodes):
            self.matrix_table.setRowHeight(i, row_height)
            for j, node2 in enumerate(nodes):
                self.matrix_table.setColumnWidth(j, column_width)
                value = self.graph.distance_matrix[node1.label][node2.label]
                display_text = "-" if value == 0 else str(value) # Replacing zero in logical matrix with dash in display
                item = QTableWidgetItem(display_text)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(items_font)
                self.matrix_table.setItem(i, j, item)


    def show_nearest_neighbour_path(self):
        start_label = self.nearest_neighbour_start_node_input.text().upper().strip()

        # Error message if the graph is empty
        if not self.graph.nodes:
            QMessageBox.warning(self, "Input Error", "The graph cannot be empty")
            return

        # Locating the starting node by the inputted label
        found = False
        for node in self.graph.nodes:
            if node.label == start_label:
                found = True
                starting_node = node
        # Error message if node doesn't exist
        if not found:
            QMessageBox.warning(self, "Input Error", "Starting Node must exist in the graph!")
            return

        # Calling Nearest Neighbour's algorithm on the constructed graph
        algorithm = NearestNeighbour(self.graph)
        output_path = algorithm.find_path(starting_node)

        # Storing logical and visual data for nodes & edges and log steps
        node_data = []
        for node in output_path.nodes:
            label = node.label
            x = node.scenePos().x()
            y = node.scenePos().y()
            node_data.append((label, x, y))
        edge_data = []
        for edge in output_path.edges:
            node1_label = edge.node1.label
            node2_label = edge.node2.label
            weight = edge.weight
            label = edge.edge_label
            edge_data.append((node1_label, node2_label, weight, label))
        log_data = output_path.log

        # Opening solution window and passing on solution's data
        self.path_window = MSTWindow(node_data, edge_data, log_data)
        self.path_window.show()

    def show_prims_MST(self):
        start_label = self.prim_start_node_input.text().upper().strip()

        # Error message if the graph is empty
        if not self.graph.nodes:
            QMessageBox.warning(self, "Input Error", "The graph cannot be empty")
            return

        # Locating the starting node by the inputted label
        found = False
        for node in self.graph.nodes:
            if node.label == start_label:
                found = True
                starting_node = node
        # Error message if node doesn't exist
        if not found:
            QMessageBox.warning(self, "Input Error", "Starting Node must exist in the graph!")
            return

        # Calling Prim's algorithm on the constructed graph
        algorithm = PrimsMST(self.graph)
        output_MST = algorithm.find_MST(starting_node)

        # Storing logical and visual data for nodes & edges and log steps
        node_data = []
        for node in output_MST.nodes:
            label = node.label
            x = node.scenePos().x()
            y = node.scenePos().y()
            node_data.append((label, x, y))
        edge_data = []
        for edge in output_MST.edges:
            node1_label = edge.node1.label
            node2_label = edge.node2.label
            weight = edge.weight
            label = edge.edge_label
            edge_data.append((node1_label, node2_label, weight, label))
        log_data = output_MST.log

        # Opening MST solution window and passing on solution's data
        self.MST_window = MSTWindow(node_data, edge_data, log_data)
        self.MST_window.show()

    def show_kruskals_MST(self):
        # Error message if the graph is empty
        if not self.graph.nodes:
            QMessageBox.warning(self, "Input Error", "The graph cannot be empty")
            return

        # Calling Kruskal's algorithm on the constructed graph
        algorithm = KruskalsMST(self.graph)
        output_MST = algorithm.find_MST()

        # Storing logical and visual data for nodes & edges and log steps
        node_data = []
        for node in output_MST.nodes:
            label = node.label
            x = node.scenePos().x()
            y = node.scenePos().y()
            node_data.append((label, x, y))
        edge_data = []
        for edge in output_MST.edges:
            node1_label = edge.node1.label
            node2_label = edge.node2.label
            weight = edge.weight
            label = edge.edge_label
            edge_data.append((node1_label, node2_label, weight, label))
        log_data = output_MST.log

        # Opening MST solution window and passing on solution's data
        self.MST_window = MSTWindow(node_data, edge_data, log_data)
        self.MST_window.show()

    def show_dijkstra_shortest_path(self):
        # Storing Start Node & End Node labels inputs (capitalising automatically)
        start_label = self.dijkstra_start_node_input.text().upper().strip()
        end_label = self.dijkstra_end_node_input.text().upper().strip()

        # Error message if label input is not a single letter
        if len(start_label) != 1 or not start_label.isalpha() or len(end_label) != 1 or not end_label.isalpha():
            QMessageBox.warning(self, "Input Error", "Node labels must be a single letter!")
            return

        # Locating the start and end nodes
        start_node = None
        for node in self.graph.nodes:
            if node.label == start_label:
                start_node = node
                break
        end_node = None
        for node in self.graph.nodes:
            if node.label == end_label:
                end_node = node
                break
        # Error messages if either of the inputted nodes aren't found
        if not start_node or not end_node:
            QMessageBox.warning(self, "Input Error", "Both nodes must exist!")
            return

        # Calling Dijkstra's algorithm on the inputted graph
        algorithm = DijkstrasShortestPath(self.graph)
        # Storing returned data for solution
        shortest_path, total_weight, labelling_orders, final_labels, working_values_list = algorithm.find_shortest_path(start_node, end_node)

        # Copy nodes logical and visuals data from the inputted graph for the shortest path graph display
        path_nodes = []
        for label in shortest_path:
            inputgraph_node = None
            # Locating node from input graph
            for node in self.graph.nodes:
                if node.label == label:
                    inputgraph_node = node
                    break
            # Copying it for the solution path display
            if inputgraph_node:
                x = inputgraph_node.scenePos().x()
                y = inputgraph_node.scenePos().y()
                node_copy = Node(label, x, y)
                path_nodes.append(node_copy)

        # Copy edges from the shortest path's logical and visuals data to pass so can be replicated in solution
        path_edges = []
        for i in range(1, len(shortest_path)):
            # Identifying edges present in the path
            node1_label = shortest_path[i - 1]
            node2_label = shortest_path[i]
            weight = self.graph.distance_matrix[node1_label][node2_label]
            # Locate nodes of the path's edges
            node1 = None
            node2 = None
            for node in path_nodes:
                if node.label == node1_label:
                    node1 = node
                elif node.label == node2_label:
                    node2 = node
            # Copying the edges for the solution path display
            if node1 and node2:
                edge = Edge(weight, node1, node2, None)
                path_edges.append(edge)

        # Storing the algorithm's solution steps for the log including Dijkstra's tables:

        # Shortest Path and its Total Weight as lines in the log ('no path' with infinity weight if doesn't exist)
        log = []
        if shortest_path:
            shortest_path_str = ""
            for label in shortest_path:
                shortest_path_str += label
        else:
            shortest_path_str = "No Path"
        log.append("Shortest Path: " + shortest_path_str)

        if total_weight == float('inf'):
            log.append("Total Weight: ∞")
        else:
            log.append("Total Weight: " + str(total_weight))

        # Storing data in Dijkstras working tables for the log (row for each node)
        table_data = []
        sorted_labels = sorted(labelling_orders.keys())

        # Storing labelling order, final label, and working values list for each node
        for label in sorted_labels:
            # Adding labelling orders
            if labelling_orders[label] is not None:
                order = labelling_orders[label]
            else:
                order = "-"
            # Adding final labels
            if final_labels[label] == float('inf'):
                final_value = "∞"
            else:
                final_value = final_labels[label]
            # Adding working values
            working_values = working_values_list[label]
            working_values_string = ""
            for value in working_values:
                working_values_string += str(value) + ", " # Working values seperated by commas
            if working_values_string.endswith(", "):
                working_values_string = working_values_string[:-2] # Remove comma from end

            # Add rows to the table for each node
            table_data.append((label, order, final_value, working_values_string))


        # Construct graph for path to display in solution window
        edge_data = []
        for edge in path_edges:
            node1_label = edge.node1.label
            node2_label = edge.node2.label
            weight = edge.weight
            edge_label = edge.edge_label
            edge_data.append((node1_label, node2_label, weight, edge_label))

        # Opening Dijkstra's solution window and pass on solution data
        self.dijkstra_window = DijkstrasWindow(path_nodes, edge_data, log, table_data)
        self.dijkstra_window.show()


