import math


class Sort:
    """The base class for sorting algorithms which will use an inputted list"""
    def __init__(self, items_list):
        self.items_list = items_list.copy()

class BubbleSort(Sort):
    """The Bubble Sort inherits from the Sort class to implement both ascending and descending sorts. The bubble sort
    is not used as an algorithm for sorting purpose at any point within the project - instead the Merge Sort is used
    since it is more efficient. However, the Bubble Sort is covered under the specification for students to
    carry out - so it has been included along with the step-by-step working.

    The Bubble Sort involves:
    - Comparing adjacent items_list in the list and swapping them if they're not in order
    - Traversing through the whole list from beginning to end carrying out adjacent swaps where needed - each traversal
    known as a pass
    - The list is sorted once we have a 'blank pass' with no swaps being made

    For the purpose of the solution log for step-by-step working, the list is written out after each pass, along with
    the number of swaps of the pass - upto and including the blank pass with no swaps."""

    def ascending(self):
        current_list = self.items_list.copy()
        log = []
        sorted = False

        # Carrying out passes until the list has been sorted
        while sorted == False:
            swaps = 0
            # Iterating through list
            for index in range(len(current_list) - 1):
                # Comparing adjacent elements
                if current_list[index] > current_list[index + 1]:
                    # Swapping if needed and updating swaps count
                    smaller = current_list[index + 1]
                    current_list[index + 1] = current_list[index]
                    current_list[index] = smaller
                    swaps += 1
            # Adding pass with number of swaps to the log
            log.append((current_list.copy(), swaps))

            # End Bubble Sort after blank pass has occurred
            if swaps == 0:
                sorted = True

        return log

    def descending(self):
        current_list = self.items_list.copy()
        log = []
        sorted = False

        # Carrying out passes until the list has been sorted
        while sorted == False:
            swaps = 0
            # Iterating through list
            for index in range(len(current_list) - 1):
                # Comparing adjacent elements
                if current_list[index] < current_list[index + 1]:
                    # Swapping if needed and updating swaps count
                    bigger = current_list[index + 1]
                    current_list[index + 1] = current_list[index]
                    current_list[index] = bigger
                    swaps += 1
            # Adding pass with number of swaps to the log
            log.append((current_list.copy(), swaps))

            # End Bubble Sort after blank pass has occurred
            if swaps == 0:
                sorted = True

        return log


class Bin:
    """Bin object is used to represent a bin container for items with a defined capacity and storage"""
    def __init__(self, capacity):
        self.capacity = capacity
        self.contents = []
        self.storage = 0

    def insert_item(self, item):
        """Inserts item into bin's contents and updates storage"""
        self.contents.append(item)
        self.storage += item


class BinPacking:
    """Contains the Bin-Packing algorithms including First-Fit, First-Fit-Decreasing and also calculating
    a Lower Bound for a bin-packing scenario."""

    def __init__(self, items_list, capacity):
        self.items_list = items_list
        self.capacity = capacity

    def lower_bound(self):
        """The Lower Bound for a scenario gives an estimation for the minimum no. of bins required to pack all items.
        The lower bound is calculated by dividing the total weight of all the items by the defined bin capacity,
        and rounding this value up."""

        # Calculating total weight of all the items
        total_weight = sum(self.items_list)
        # Dividing total weight by bin capacity and then rounding up for the lower bound
        lower_bound_value = math.ceil(total_weight / self.capacity)

        return total_weight, self.capacity, lower_bound_value

    def first_fit(self):
        """The First-Fit algorithm works by taking each item and traversing through the bins and seeing the
        first bin in which it would fit. If it cannot fit in the existing bins, a new bin is created.
        This is repeated until all the items have been packed into bins."""

        bins = []

        # Traversing through the inputted list until all items have been added to bins
        for item in self.items_list:
            placed = False

            # Traversing through the bins
            for bin in bins:
                # Adding item to a bin if there is enough space and terminating traversal
                if bin.storage + item <= bin.capacity:
                    bin.insert_item(item)
                    placed = True
                    break

            # Creating a new bin if it could not be placed into any of the existing bins
            if not placed:
                new_bin = Bin(self.capacity)
                new_bin.insert_item(item)
                bins.append(new_bin)

        return bins


    def first_fit_decreasing(self):
        """The First-Fit-Decreasing algorithm works by first sorting the list into descending order and then carrying
        out the First-Fit algorithm on the sorted list. In exam questions, the descending sort is done using a
        bubble sort which the students must carry out, so this has been incorporated into the First-Fit-Decreasing
        solution."""

        # Sorting the list into descending order via bubble sort
        sorter = BubbleSort(self.items_list)
        sort_log = sorter.descending()
        sorted_list = sort_log[-1][0]

        # Carrying out first-fit on the sorted list with the inputted bin capacity
        bins = BinPacking(sorted_list, self.capacity).first_fit()

        return sort_log, sorted_list, bins


