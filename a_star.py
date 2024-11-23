def is_valid(point: tuple[int, int], rows: int, cols: int) -> bool:
    """
    Checks if a cell is within the grid boundaries.

    :param point: (row, col) - the point to check
    :param rows: number of rows
    :param cols: number of columns

    :return: True if the cell is within the grid boundaries, False otherwise
    """
    # TODO: add doctests to all functions


def is_destination(point: tuple[int, int], dest):
    """
    Checks if a cell is the destination.

    :param point: (row, col) - the point to check
    :param dest: (row, col) - the destination cell

    :return: True if the cell is the destination cell, False otherwise
    """


def calculate_h_value(point: tuple[int, int], dest):
    """
    Calculates the heuristic value (Euclidean distance) from a cell to the destination.

    Parameters:
        dest (list of int): Coordinates of the destination [row, col].

    Returns:
        float: Heuristic value (distance to the destination).
    """
    # TODO: rewrite documentstion


def trace_path(cell_details, dest):
    """
    Traces and prints the path from the source to the destination.

    Parameters:
        cell_details (dict): Dictionary storing details of each cell.
        dest (list of int): Coordinates of the destination [row, col].
    """
def calculate_height_cost(current_height: float, next_height: float) -> float:
    """
    Calculate movement cost based on elevation change.
    Equal cost for uphill and downhill movements.
    
    Args:
        current_height: Height of current node
        next_height: Height of next node
    
    Returns:
        Cost of movement considering absolute height difference
    """
    return abs(next_height - current_height)


def a_star_search(grid, src, dest):
    """
    Implements the A* search algorithm to find the shortest path.

    Parameters:
        grid (list of list of int): The grid representing the map (1 for unblocked, 0 for blocked).
        src (list of int): Coordinates of the source [row, col].
        dest (list of int): Coordinates of the destination [row, col].
    """
