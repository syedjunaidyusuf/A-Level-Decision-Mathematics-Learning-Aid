from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from Graphs_MainInterface import GraphAlgorithmsWindow
from SimpleAlgorithms_Interface import SimpleAlgorithmsWindow


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        # Creating window
        self.setWindowTitle("Decision Mathematics Learning Aid")
        self.setGeometry(200, 200, 500, 400)

        # Central widget & layout
        central = QWidget()
        central.setStyleSheet("background-color: #DCF0FF;")
        layout = QVBoxLayout()
        central.setLayout(layout)
        self.setCentralWidget(central)

        # Setting title
        title = QLabel("Decision Mathematics Learning Aid")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Comic Sans', 45, QFont.Bold))
        layout.addWidget(title)
        layout.addSpacing(30)

        # Buttons style
        btn_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 60px;
                font-weight: bold;
                border-radius: 25px;
                padding: 12px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

        # Simple Algorithms button
        self.simple_algorithms_button = QPushButton("Simple Algorithms")
        self.simple_algorithms_button.setStyleSheet(btn_style)
        self.simple_algorithms_button.clicked.connect(self.open_simple_algorithms)
        self.simple_algorithms_button.setFixedWidth(1000)
        self.simple_algorithms_button.setFixedHeight(150)
        layout.addWidget(self.simple_algorithms_button, alignment=Qt.AlignHCenter)
        layout.addSpacing(40)

        # Graph Algorithms button
        self.graph_algorithms_button = QPushButton("Graph Algorithms")
        self.graph_algorithms_button.setStyleSheet(btn_style)
        self.graph_algorithms_button.clicked.connect(self.open_graph_algorithms)
        self.graph_algorithms_button.setFixedWidth(1000)
        self.graph_algorithms_button.setFixedHeight(150)
        layout.addWidget(self.graph_algorithms_button, alignment=Qt.AlignHCenter)
        layout.addSpacing(40)


    def open_simple_algorithms(self):
        self.simple_algorithms_window = SimpleAlgorithmsWindow()
        self.simple_algorithms_window.showMaximized()

    def open_graph_algorithms(self):
        self.graph_algorithms_window = GraphAlgorithmsWindow()
        self.graph_algorithms_window.showMaximized()


