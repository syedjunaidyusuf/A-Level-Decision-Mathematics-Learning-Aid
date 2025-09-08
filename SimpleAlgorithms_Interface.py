from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout, QMessageBox, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from SimpleAlgorithms import BubbleSort, BinPacking


class SimpleAlgorithmsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Algorithms")
        self.resize(800, 600)

        # Setting styles
        application_font = QFont('Comic Sans', 12)
        self.setFont(application_font)
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 30px;
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
            QMessageBox {
                font-family: 'Comic Sans MS';
                font-size: 12px;
            }
        """)

        self._create_interface()

    def _create_interface(self):
        main_layout = QVBoxLayout(self)

        # Creating Input List title label
        input_list_label = QLabel("Input List:")
        input_list_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(input_list_label)
        # Creating Input List interface (12 boxes)
        self.input_boxes = []
        input_boxes_layout = QHBoxLayout()
        input_boxes_layout.setSpacing(10)

        for box in range(12):
            input_box = QLineEdit()
            input_box.setFixedSize(80, 50)
            input_box.setAlignment(Qt.AlignCenter)
            self.input_boxes.append(input_box)
            input_boxes_layout.addWidget(input_box)
        main_layout.addLayout(input_boxes_layout)
        main_layout.addSpacing(15)

        # Bubble Sort Buttons
        ascending_sort_button = QPushButton("Bubble Sort Ascending")
        descending_sort_button = QPushButton("Bubble Sort Descending")
        ascending_sort_button.clicked.connect(self.sort_ascending)
        descending_sort_button.clicked.connect(self.sort_descending)

        sort_buttons_layout = QHBoxLayout()
        sort_buttons_layout.setSpacing(30)

        sort_buttons_layout.addWidget(ascending_sort_button)
        sort_buttons_layout.addWidget(descending_sort_button)

        main_layout.addLayout(sort_buttons_layout)
        main_layout.addSpacing(25)

        # Bin Capacity input textbox
        capacity_layout = QHBoxLayout()
        capacity_layout.setSpacing(10)
        label_bin_capacity = QLabel("Bin Capacity:")
        label_bin_capacity.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.capacity_field = QLineEdit()
        self.capacity_field.setFixedSize(120, 50)
        self.capacity_field.setAlignment(Qt.AlignCenter)
        capacity_layout.addWidget(label_bin_capacity)
        capacity_layout.addWidget(self.capacity_field)
        capacity_layout.addStretch()
        main_layout.addLayout(capacity_layout)
        main_layout.addSpacing(15)

        # Bin-packing buttons
        first_fit_button = QPushButton("First Fit")
        first_fit_decreasing_button = QPushButton("First Fit Decreasing")
        lower_bound_button = QPushButton("Calculate Lower Bound")

        for button in (first_fit_button, first_fit_decreasing_button, lower_bound_button):
            button.setStyleSheet(
                "background-color: #2196F3; color: white;"
                " font-weight: bold; border-radius: 15px;"
            )

        first_fit_button.clicked.connect(self.first_fit)
        first_fit_decreasing_button.clicked.connect(self.first_fit_decreasing)
        lower_bound_button.clicked.connect(self.calc_lower_bound)

        bin_buttons_layout = QHBoxLayout()
        bin_buttons_layout.setSpacing(20)

        bin_buttons_layout.addWidget(first_fit_button)
        bin_buttons_layout.addWidget(first_fit_decreasing_button)
        bin_buttons_layout.addWidget(lower_bound_button)

        main_layout.addLayout(bin_buttons_layout)
        main_layout.addSpacing(25)

        # Output log
        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        self.output_log.setStyleSheet("""
            QTextEdit {
                border: 2px solid gray;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        main_layout.addWidget(self.output_log)

    def _read_input_list(self):
        items = []

        # Iterating through boxes to retrieve the list's items
        for position, input_box in enumerate(self.input_boxes, start=1):
            # Take inputted text from the box
            item_text = input_box.text().strip()

            # Skip empty textbox
            if not item_text:
                continue
            # Add item to list from the textbox
            try:
                items.append(int(item_text))
            # Error message if input not an integer
            except ValueError:
                raise ValueError(f"Item #{position} ('{item_text}') is not an integer.")

        # Error message in case of empty list
        if not items:
            raise ValueError("Please enter at least one integer.")

        return items

    def _read_capacity(self):
        # Take inputted bin capacity from the box
        item_text = self.capacity_field.text().strip()

        # Error message if empty bin capacity
        if not item_text:
            raise ValueError("Please enter a bin capacity.")
        # Store capacity if inputted
        try:
            capacity = int(item_text)
        # Error message if inputted capacity not an integer
        except ValueError:
            raise ValueError("Bin capacity must be an integer.")
        # Error message if inputted capacity not positive
        if capacity <= 0:
            raise ValueError("Bin capacity must be positive.")

        return capacity

    def _display_bubblesort_log(self, original_list, log):
        self.output_log.clear()
        # Write out original list first
        self.output_log.append(f"<b>{original_list}</b>")
        self.output_log.append("")
        self.output_log.append("")
        # Write number of swaps after the state of the list after each pass
        for state, swaps in log:
            self.output_log.append(f"{state}   →   {swaps} swaps")
            self.output_log.append("")
        # Display that sort is complete (after blank pass)
        self.output_log.append("No Swaps - Sort Complete")

    def sort_ascending(self):
        # Retrieve items for the sort from the textboxes
        try:
            items = self._read_input_list()
        # Display error message if needed
        except ValueError as error:
            QMessageBox.warning(self, "Input Error", str(error))
            return

        # Carry out Ascending Bubble Sort and display log with working steps
        sorter = BubbleSort(items)
        log = sorter.ascending()
        self._display_bubblesort_log(items, log)

    def sort_descending(self):
        # Retrieve items for the sort from the textboxes
        try:
            items = self._read_input_list()
        # Display error message if needed
        except ValueError as error:
            QMessageBox.warning(self, "Input Error", str(error))
            return

        # Carry out Descending Bubble Sort and display log with working steps
        sorter = BubbleSort(items)
        log = sorter.descending()
        self._display_bubblesort_log(items, log)

    def first_fit(self):
        # Retrieve items for the bin-packing from the textboxes
        try:
            items = self._read_input_list()
            capacity_value = self._read_capacity()
        # Display error message if needed for invalid list
        except ValueError as error:
            QMessageBox.warning(self, "Input Error", str(error))
            return
        # Display error message if a list item is larger than the bin capacity
        for position, weight in enumerate(items, start=1):
            if weight > capacity_value:
                QMessageBox.warning(self, "Input Error",
                                    f"Item #{position} of weight {weight} cannot be larger than the Bin Capacity")
                return

        # Carry out First-Fit Bin-Packing
        bin_packer = BinPacking(items, capacity_value)
        bins = bin_packer.first_fit()

        # Display steps in the log
        self.output_log.clear()
        for bin_index, bin in enumerate(bins, start=1):
            self.output_log.append(f"<b>Bin {bin_index}:</b> {bin.contents}")
            self.output_log.append("")

    def first_fit_decreasing(self):
        # Retrieve items for the bin-packing from the textboxes
        try:
            items = self._read_input_list()
            capacity_value = self._read_capacity()
        # Display error message if needed for invalid list
        except ValueError as error:
            QMessageBox.warning(self, "Input Error", str(error))
            return
        # Display error message if a list item is larger than the bin capacity
        for position, weight in enumerate(items, start=1):
            if weight > capacity_value:
                QMessageBox.warning(self, "Input Error",
                                    f"Item #{position} of weight {weight} cannot be larger than the Bin Capacity")
                return

        # Carrying out First-Fit Decreasing Bin-Packing
        bin_packer = BinPacking(items, capacity_value)
        sort_log, sorted_list, bins = bin_packer.first_fit_decreasing()

        # Displaying Bubble Sort working
        self._display_bubblesort_log(items, sort_log)
        self.output_log.append("")
        # Writing out sorted list after carried out Bubble Sort
        self.output_log.append(f"<b>Sorted List: {sorted_list}</b>")
        self.output_log.append("")

        # Displaying the bins after First-Fit carried out on the sorted list
        for bin_index, bin in enumerate(bins, start=1):
            self.output_log.append(f"<b>Bin {bin_index}:</b> {bin.contents}")
            self.output_log.append("")

    def calc_lower_bound(self):
        # Retrieve items for the bin-packing from the textboxes
        try:
            items = self._read_input_list()
            capacity_value = self._read_capacity()
        # Display error message if needed for invalid list
        except ValueError as error:
            QMessageBox.warning(self, "Input Error", str(error))
            return
        # Display error message if a list item is larger than the bin capacity
        for position, weight in enumerate(items, start=1):
            if weight > capacity_value:
                QMessageBox.warning(self, "Input Error",
                                    f"Item #{position} of weight {weight} cannot be larger than the Bin Capacity")
                return

        # Calculating Lower Bound for the scenario
        total_weight, capacity_value, lower_bound_value = BinPacking(items, capacity_value).lower_bound()
        ratio = total_weight / capacity_value

        # Displaying the log steps including the calculation result to 3dp if decimal
        self.output_log.clear()
        if ratio.is_integer():
            self.output_log.append(
                f"Total Weights / Bin Capacity = {total_weight} / {capacity_value} = {int(ratio)}")
        else:
            self.output_log.append(
                f"Total Weights / Bin Capacity = {total_weight} / {capacity_value} = {ratio:.3f}…")
        # Writing out the final lower bound (rounded up from calculation)
        self.output_log.append(f"<b>Lower Bound = {lower_bound_value}</b>")


