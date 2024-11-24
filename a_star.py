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


def trace_path(cell_details, dest) -> list[tuple]:
    """
    Finds the path from the destination to the start using parent information.

    Parameters:
        cell_details: A grid (2D list) where each cell contains a tuple (parent_row, parent_col).
        dest: Coordinates of the destination cell as (row, col).

    Returns:
        The path as a list of coordinates [(row, col), ...].
    Examples:
        >>> cell_details = [
        ...     [(0, 0), (0, 0), (0, 1)],
        ...     [(0, 0), (0, 1), (1, 1)],
        ...     [(1, 2), (1, 2), (2, 1)]
        ... ]
        >>> dest = (2, 2)
        >>> trace_path(cell_details, dest)
        [(0, 0), (0, 1), (1, 1), (1, 2), (2, 1), (2, 2)]
    """
    path = []
    while cell_details[dest[0]][dest[1]] != dest:
        path.append(dest)
        dest = cell_details[dest[0]][dest[1]]
    return list(reversed(path+[dest]))



def a_star_search(grid, src, dest):
    """
    Implements the A* search algorithm to find the shortest path.

    Parameters:
        grid (list of list of int): The grid representing the map (1 for unblocked, 0 for blocked).
        src (list of int): Coordinates of the source [row, col].
        dest (list of int): Coordinates of the destination [row, col].
    """
