from PyQt5.QtWidgets import QMainWindow, QSplitter, QGraphicsScene, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt

from GraphStructure import Node, Edge
from Graphs_View import GraphView


class MSTWindow(QMainWindow):
    def __init__(self, node_data, edge_data, log_data):
        super().__init__()
        self.setWindowTitle("MST Solution")
        self.setGeometry(150, 150, 800, 600)
        splitter = QSplitter(Qt.Vertical)
        self.scene = QGraphicsScene(self)

        # Adding solution graph read-only canvas to window's splitter
        self.view = GraphView(self.scene, self)
        splitter.addWidget(self.view)

        # Adding read-only log for working steps to window's splitter
        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.setStyleSheet("""
            QTextEdit {
                font-family: 'Comic Sans MS', Comic Sans, cursive;
                font-size: 30px;
                color: black;
                background-color: white;
            }
        """)
        self.log_widget.setPlainText("\n".join(log_data))
        splitter.addWidget(self.log_widget)

        # Customising splitter
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)


        self.node_map = {} # Dictionary to map node labels to its objects in the MST

        # Adding MST's nodes to solution graph display
        for label, x, y in node_data:
            new_node = Node(label, x, y)
            self.scene.addItem(new_node)
            self.node_map[label] = new_node
        # Adding MST's edges to solution graph display
        for node1_label, node2_label, weight, edge_label in edge_data:
            node1 = self.node_map[node1_label]
            node2 = self.node_map[node2_label]
            new_edge = Edge(weight, node1, node2, self.scene)
            new_edge.edge_label = edge_label
            self.scene.addItem(new_edge)


class DijkstrasWindow(QMainWindow):
    def __init__(self, node_data, edge_data, log, dijkstras_table_data):
        super().__init__()
        self.setWindowTitle("Dijkstra's Shortest Path Solution")
        self.setGeometry(150, 150, 800, 600)
        splitter = QSplitter(Qt.Vertical)
        self.scene = QGraphicsScene(self)
        self.view = GraphView(self.scene, self)
        splitter.addWidget(self.view)

        # Log for solution path and its weight
        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.setStyleSheet("""
            QTextEdit {
                font-family: 'Comic Sans MS', Comic Sans, cursive;
                font-size: 30px;
                color: black;
                background-color: white;
            }
        """)
        self.log_widget.setPlainText("\n".join(log))
        splitter.addWidget(self.log_widget)

        # Dijkstras Tables for solution:
        # Initialising empty table
        self.dijkstras_table = QTableWidget()
        self.dijkstras_table.setColumnCount(4)
        self.dijkstras_table.setHorizontalHeaderLabels(["Node", "Labelling Order", "Final Value", "Working Values"])
        self.dijkstras_table.setRowCount(len(dijkstras_table_data))
        # Filling in table
        for i, (node_label, labelling_order, final_value, working_values_string) in enumerate(dijkstras_table_data):
            self.dijkstras_table.setItem(i, 0, QTableWidgetItem(str(node_label)))
            self.dijkstras_table.setItem(i, 1, QTableWidgetItem(str(labelling_order)))
            self.dijkstras_table.setItem(i, 2, QTableWidgetItem(str(final_value)))
            self.dijkstras_table.setItem(i, 3, QTableWidgetItem(str(working_values_string)))
        # Table styles
        self.dijkstras_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.dijkstras_table.setStyleSheet("""
            QTableWidget {
                font-family: 'Comic Sans MS', Comic Sans, cursive;
                font-size: 25px;
                background-color: white;
            }
            QHeaderView::section {
                font-family: 'Comic Sans MS', Comic Sans, cursive;
                font-size: 25px;
                background-color: white;
                border: 1px solid black;
            }
        """)
        splitter.addWidget(self.dijkstras_table)

        # Splitter customisations
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 1)
        self.setCentralWidget(splitter)


        self.node_map = {} # Dictionary to map node labels to its objects in the solution path
        # Adding path's nodes to solution graph display
        for node in node_data:
            self.scene.addItem(node)
            self.node_map[node.label] = node
        # Adding path's edges to solution graph display
        for n1_label, n2_label, weight, edge_label in edge_data:
            n1 = self.node_map[n1_label]
            n2 = self.node_map[n2_label]
            new_edge = Edge(weight, n1, n2, self.scene)
            new_edge.edge_label = edge_label
            self.scene.addItem(new_edge)
