"""
A* searching algorithm"""
import math

def is_in_grid(point: tuple[int, int], rows: int, cols: int) -> bool:
    """
    Checks if a cell is within the grid boundaries.

    :param point: (row, col) - the point to check
    :param rows: number of rows
    :param cols: number of columns

    :return: True if the cell is within the grid boundaries, False otherwise

    >>> is_in_grid((1, 1), 3, 3)
    True
    >>> is_in_grid((3, 3), 3, 3)
    False
    >>> is_in_grid((-1, 2), 3, 3)
    False
    >>> is_in_grid((2, 2), 3, 3)
    True
    """
    row, col = point
    return 0 <= row < rows and 0 <= col < cols

def is_destination(point: tuple[int, int], dest: tuple[int, int]) -> bool:
    """
    Checks if a cell is the destination.

    :param point: (row, col) - the point to check
    :param dest: (row, col) - the destination cell

    :return: True if the cell is the destination cell, False otherwise

    >>> is_destination((2, 3), (2, 3))
    True
    >>> is_destination((1, 2), (2, 3))
    False
    >>> is_destination((0, 0), (0, 0))
    True
    >>> is_destination((3, 4), (2, 3))
    False
    """
    return point == dest

def calculate_h_value(point: tuple[int, int], dest: tuple[int, int]) -> float:
    """
    Calculates the heuristic value (Euclidean distance) from a cell to the destination.

    :param point: (row, col) - the current cell
    :param dest: (row, col) - the destination cell

    :return: Heuristic value (Euclidean distance to the destination)

    >>> calculate_h_value((0, 0), (3, 4))
    7
    >>> calculate_h_value((1, 2), (2, 3))
    2
    >>> calculate_h_value((0, 0), (0, 0))
    0
    >>> calculate_h_value((3, 3), (0, 0))
    6
    """
    row, col = point
    dest_row, dest_col = dest
    return abs(row - dest_row) + abs(col - dest_col)



def trace_path(cell_details, dest):
    """
    Traces and prints the path from the source to the destination.

    Parameters:
        cell_details (dict): Dictionary storing details of each cell.
        dest (list of int): Coordinates of the destination [row, col].
    """


def a_star_search(grid, src, dest):
    """
    Implements the A* search algorithm to find the shortest path.

    Parameters:
        grid (list of list of int): The grid representing the map (1 for unblocked, 0 for blocked).
        src (list of int): Coordinates of the source [row, col].
        dest (list of int): Coordinates of the destination [row, col].
    """


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
