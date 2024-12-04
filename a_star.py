"""
A* searching algorithm
"""

from heapq import heappop, heappush
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



def trace_path(cell_details, dest) -> list[tuple]:
    """
    Finds the path from the destination to the start using parent information.

    Parameters:
        cell_details: A grid (2D list) where each cell contains a tuple (parent_row, parent_col).
        dest: Coordinates of the destination cell as (row, col).

    Returns:
        The path as a list of coordinates [(row, col), ...].

    Examples:
    >>> cell_details = [[{'parent': None}, {'parent': (0, 0)}, {'parent': (0, 1)}], \
                        [{'parent': (0, 0)}, {'parent': (1, 0)}, {'parent': (1, 1)}], \
                        [{'parent': (1, 0)}, {'parent': (2, 0)}, {'parent': (2, 1)}]]
    >>> trace_path(cell_details, (2, 2))
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    >>> cell_details = [[{'parent': None}, {'parent': (0, 0)}], \
                        [{'parent': (0, 0)}, {'parent': (1, 0)}]]
    >>> trace_path(cell_details, (1, 1))
    [(0, 0), (1, 0), (1, 1)]
    >>> cell_details = [[{'parent': None}]]
    >>> trace_path(cell_details, (0, 0))
    [(0, 0)]
    """
    path = []
    while cell_details[dest[0]][dest[1]]['parent'] is not None:
        path.append(dest)
        dest = cell_details[dest[0]][dest[1]]['parent']
    return list(reversed(path+[dest]))


def calculate_height_cost(current_height: float, next_height: float) -> float:
    """
    Calculate movement cost based on elevation change.
    Equal cost for uphill and downhill movements.
    
    Args:
        current_height: Height of current node
        next_height: Height of next node
    
    Returns:
        Cost of movement considering absolute height difference
    >>> calculate_height_cost(9, 10)
    1
    """
    return abs(next_height - current_height)


def a_star_1(open_list, dest, directions, rows, cols, closed_list, grid, cell_details):
    while open_list:
        _, current = heappop(open_list)
        row, col = current
        if (row, col) == dest:
            return trace_path(cell_details, dest)
        closed_list[row][col] = True
        for dy, dx in directions:
            new_row, new_col = row + dy, col + dx
            if not is_in_grid((new_row, new_col), rows, cols):
                continue
            if closed_list[new_row][new_col]:
                continue
            movement_cost = calculate_height_cost(
                grid[row][col],
                grid[new_row][new_col]
            )
            if abs(dy) == 1 and abs(dx) == 1:
                movement_cost *= math.sqrt(2)
            g_new = cell_details[row][col]['g'] + movement_cost
            h_new = calculate_h_value((new_row, new_col), dest)
            f_new = g_new + h_new
            if cell_details[new_row][new_col]['f'] > f_new:
                heappush(open_list, (f_new, (new_row, new_col)))
                cell_details[new_row][new_col] = {
                    'g': g_new,
                    'h': h_new,
                    'f': f_new,
                    'parent': (row, col)
                }
    return None    

def a_star_search_with_height(grid: list[list[float]],
                            src: tuple[int, int],
                            dest: tuple[int, int]) -> list[tuple[int, int]] | None:
    """
    A* Search Algorithm with equal costs for uphill and downhill movement.
    
    Args:
        grid: 2D list of heights for each cell
        src: Starting coordinates (row, col)
        dest: Destination coordinates (row, col)
    
    Returns:
        List of coordinates representing the path, or None if no path exists
    >>> grid = [\
        [1.0, 1.2, 2.0, 3.0, 2.5],\
        [1.1, 1.8, 2.3, 2.5, 2.0],\
        [1.3, 2.0, 3.0, 2.0, 1.5],\
        [1.7, 2.2, 2.5, 1.5, 1.0],\
        [2.0, 2.5, 2.0, 1.2, 1.0]]
    >>> src = (0, 0)
    >>> dest = (4, 4)
    >>> a_star_search_with_height(grid, src, dest)
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    """
    rows, cols = len(grid), len(grid[0])
    if not (is_in_grid(src, rows, cols) and
            is_in_grid(dest, rows, cols)):
        return None
    open_list = []
    closed_list = [[False for _ in range(cols)] for _ in range(rows)]
    cell_details = [[{
        'g': float('inf'),
        'h': float('inf'),
        'f': float('inf'),
        'parent': None
    } for _ in range(cols)] for _ in range(rows)]
    start_row, start_col = src
    cell_details[start_row][start_col] = {
        'g': 0,
        'h': calculate_h_value(src, dest),
        'f': calculate_h_value(src, dest),
        'parent': None
    }
    heappush(open_list, (0, src))
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]
    arg = a_star_1((open_list, dest, directions, rows, cols, closed_list, grid, cell_details))
    return arg
    # while open_list:
    #     _, current = heappop(open_list)
    #     row, col = current
    #     if (row, col) == dest:
    #         return trace_path(cell_details, dest)
    #     closed_list[row][col] = True
    #     for dy, dx in directions:
    #         new_row, new_col = row + dy, col + dx
    #         if not is_in_grid((new_row, new_col), rows, cols):
    #             continue
    #         if closed_list[new_row][new_col]:
    #             continue
    #         movement_cost = calculate_height_cost(
    #             grid[row][col],
    #             grid[new_row][new_col]
    #         )
    #         if abs(dy) == 1 and abs(dx) == 1:
    #             movement_cost *= math.sqrt(2)
    #         g_new = cell_details[row][col]['g'] + movement_cost
    #         h_new = calculate_h_value((new_row, new_col), dest)
    #         f_new = g_new + h_new
    #         if cell_details[new_row][new_col]['f'] > f_new:
    #             heappush(open_list, (f_new, (new_row, new_col)))
    #             cell_details[new_row][new_col] = {
    #                 'g': g_new,
    #                 'h': h_new,
    #                 'f': f_new,
    #                 'parent': (row, col)
    #             }
    # return None
if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
