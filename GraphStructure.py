import math

from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtGui import QFont, QPen
from PyQt5.QtCore import Qt, QPointF, QLineF


class Graph:
    """This class represents the entire graph structure, managing its nodes & edges stored as a list of objects
     and its distance matrix, which is stored efficiently as a dictionary of dictionaries. The collection of nodes and
     edges is what defines the graph, and the matrix is updated and stored accordingly. The class includes
     methods to edit and update the graph by adding & deleting nodes and edges. It only handles the logical storing
     of the graph with its nodes, edges and distance matrix, since the display is handled in the interface file

    The distance matrix is stored as a nested dictionary (dictionary of dictionaries):
    Each node has its own nested dictionary, where the keys store the labels of the other nodes and the values store
    the weights of edges between them (stored as zero if none)"""

    def __init__(self):
        self.nodes = [] # List of node objects of graph
        self.edges = [] # List of edge objects of graph
        self.distance_matrix = {} # Stored as nested dictionary (dictionary of dictionaries)
        self.total_weight = 0 # Sum of all the edge weights - useful in algorithms

        self.log = [] # Used to log the steps of algorithms as array of strings for each line to display working

    def add_node(self, new_node):
        """Adds a new node to the logical graph, then initialises its row & column within the distance matrix."""
        # Adding node to the logical graph structure
        self.nodes.append(new_node)

        # Update distance matrix with new node:
        self.distance_matrix[new_node.label] = {} # Creates a new empty row (nested dictionary) for new node
        for node in self.nodes:
            self.distance_matrix[new_node.label][node.label] = 0 # Initialises new node's row with other nodes of the graph
            self.distance_matrix[node.label][new_node.label] = 0 # Adds new node to the rows/dictionaries of existing nodes

    def delete_node(self, removal_node):
        """Deletes a node from the logical graph, also deleting the connected edges,
        then deletes its row & column from the distance matrix."""
        # Deleting the node from the logical graph structure
        self.nodes.remove(removal_node)

        # Removing all connected edges from the node
        for edge in removal_node.edges[:]:
            self.delete_edge(edge)

        # Update distance matrix with node deleted
        del self.distance_matrix[removal_node.label]  # Deletes the row (nested dictionary) of the node being removed
        for node in self.nodes:
            del self.distance_matrix[node.label][removal_node.label] # Deletes node being removed from other nodes' rows (nested dictionaries)


    def add_edge(self, new_edge):
        """Adds an edge to the logical graph, updating its total weight, then assigns the edge weight to the relevant
        value in the distance matrix."""
        # Adding edge to logical graph structure
        self.edges.append(new_edge)
        self.total_weight += new_edge.weight

        # Update distance matrix with new edge:
        self.distance_matrix[new_edge.node1.label][new_edge.node2.label] = new_edge.weight
        self.distance_matrix[new_edge.node2.label][new_edge.node1.label] = new_edge.weight


    def delete_edge(self, removal_edge):
        """Deletes an edge from the logical graph, updating its total weight, and then deletes the edge also from the
         node objects. Finally, deletes the edge weight from the relevant value in the distance matrix."""
        # Deleting edge from logical graph structure and the nodes it's connected to
        self.edges.remove(removal_edge)
        removal_edge.node1.edges.remove(removal_edge)
        removal_edge.node2.edges.remove(removal_edge)
        self.total_weight -= removal_edge.weight

        # Update adjacency matrix with edge deleted
        self.distance_matrix[removal_edge.node1.label][removal_edge.node2.label] = 0
        self.distance_matrix[removal_edge.node2.label][removal_edge.node1.label] = 0


class Node(QGraphicsEllipseItem):
    """Nodes of a graph are stored as objects of this 'Node' class. The nodes are identified by their 'label' attribute,
    which stores the inputted node label as a single letter. The edge class includes attributes to both:
    - Logically represent it within the graph structure, including its valency and connected nodes/edges
    - Graphically display the node through PyQt by inheriting QGraphicsEllipse Item in order to display it as a
    draggable circle with its label centred on it"""

    def __init__(self, label, x, y):
        # Logical Node
        self.label = label # Node label as a single letter
        self.edges = [] # List of the edge objects connected to the node
        self.valency = 0 # Sum of weights of connected edges - used during algorithms

        # Node dimensions
        self.diameter = 60

        # Creating and drawing node as a draggable ellipse:
        super().__init__(0, 0, self.diameter, self.diameter)
        self.setBrush(Qt.green)
        self.setPen(QPen(Qt.black, 2))
        self.setPos(x - self.diameter/2, y - self.diameter/2)
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)

        # Node's label as text centred on the node:
        self.label_text = QGraphicsTextItem(label, self)
        self.label_text.setFont(QFont("Arial", 20))
        self.label_text.setDefaultTextColor(Qt.black)
        self.label_text.setPos(self.rect().center() - self.label_text.boundingRect().center())

    def add_edge(self, edge):
        """Called when an edge is added to the node: adds edge to the 'edges' attribute and updates valency"""
        self.edges.append(edge)
        self.valency += edge.weight

    # Updating label and edges positions
    def mouseMoveEvent(self, event):
        """Called when the mouse moves something on the display: updates the node & its label on the screen and
        calls the edges update method so their display is also updated"""
        super().mouseMoveEvent(event)
        self.label_text.setPos(self.rect().center() - self.label_text.boundingRect().center())
        for edge in self.edges:
            edge.update_position()


class Edge(QGraphicsLineItem):
    """Edges of a graph are stored as objects of this 'Edge' class. For the purpose of this program, the edges are
    stored as weighted connections between two nodes. The edge class includes attributes and methods to both:
    - Logically represent it within the graph structure, including its node connections and weights
    - Graphically display the edge through PyQt by inheriting QGraphicsLineItem in order to display it as a line
    between its two nodes (between the circumferences of the nodes)
    - Display its weight as a label of text which lies above the edge-line on its perpendicular bisector"""

    def __init__(self, weight, node1, node2, scene):
        super().__init__() # Inherit QGraphicsLine to draw edge as a line

        # Logical Edge
        self.weight = weight
        self.node1 = node1
        self.node2 = node2
        self.nodes = [node1, node2] # The node objects the edge connects
        # Adding edge to its nodes
        self.node1.add_edge(self)
        self.node2.add_edge(self)

        self.edge_label = f"{node1.label}{node2.label}({weight})" # Label in format AB(5) to use in displaying working

        # Displaying edge as line between its two nodes
        self.scene = scene
        self.setPen(QPen(Qt.black, 3))
        if self.scene is not None:
            self.scene.addItem(self)

        # Edge weight as a label of text above it
        self.weight_text = QGraphicsTextItem(str(weight))
        self.weight_text.setFont(QFont("Comic Sans", 15))
        self.weight_text.setDefaultTextColor(Qt.black)
        if self.scene is not None:
            self.scene.addItem(self.weight_text)

        # Update Position of edge and its weight
        self.update_position()

    def update_position(self):
        """Updates the edge line's position to lie on the line between the centres of its two connected nodes, but end
        on the circumferences of the nodes.
        The method also involves updating the position of the weight of the edge, which should be positioned slightly
        above the centre of the edge line and must lie on the perpendicular bisector.
        Although they may seem simpler than they are, both of these processes need complex trigonometry formulae
        for the cleanest visuals to match exam questions."""

        # Centres of the nodes and finding radius
        x1 = self.node1.scenePos().x() + self.node1.diameter / 2
        y1 = self.node1.scenePos().y() + self.node1.diameter / 2
        x2 = self.node2.scenePos().x() + self.node2.diameter / 2
        y2 = self.node2.scenePos().y() + self.node2.diameter / 2
        radius = self.node1.diameter / 2

        # Original full line without edges trimmed
        full_line = QLineF(x1, y1, x2, y2)
        line_length = full_line.length()

        # To avoid crash due to division by zero
        if line_length == 0:
            return

        # Trim both ends by node radius to ensure the edges end on their circumferences and do not reach inside the node
        offset_dx = (x2 - x1) / line_length * radius
        offset_dy = (y2 - y1) / line_length * radius
        trimmed_start = QPointF(x1 + offset_dx, y1 + offset_dy)
        trimmed_end = QPointF(x2 - offset_dx, y2 - offset_dy)
        self.setLine(QLineF(trimmed_start, trimmed_end))

        # Setting Weight label to lie on the perpendicular bisector
        mid_x = (trimmed_start.x() + trimmed_end.x()) / 2
        mid_y = (trimmed_start.y() + trimmed_end.y()) / 2

        # Calculating length as hypotenuse of the dx and dy of the trimmed edge lines (to end on node circumferences)
        dx = trimmed_end.x() - trimmed_start.x()
        dy = trimmed_end.y() - trimmed_start.y()
        perp_length = math.hypot(dx, dy)

        if perp_length == 0:
            offset_x = 0
            offset_y = 0
        else:
            offset_x = -dy / perp_length * 20
            offset_y = dx / perp_length * 20

        # Assigning calculated position of trimmed edges
        self.weight_text.setPos(mid_x + offset_x - self.weight_text.boundingRect().width() / 2,
                                mid_y + offset_y - self.weight_text.boundingRect().height() / 2)


class DummyLogicalEdge:
    """Stores an edge logically without displaying which is used by algorithms to test if it creates a cycle"""

    def __init__(self, weight, node1, node2):
        self.weight = weight
        self.node1 = node1
        self.node2 = node2
        self.edge_label = f"{node1.label}{node2.label}({weight})" # Label in format AB(5) to use in displaying working
        self.nodes = [node1, node2] # Node objects the edge connects

