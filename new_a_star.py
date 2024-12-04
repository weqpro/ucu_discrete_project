from heapq import heappush, heappop
import math

import numpy as np


def trace_path(node, nodes):
    result = [node]
    parent = nodes[node][2:]
    while parent is not None:
        result.append(parent)
        parent = nodes[parent][2:]
    return result


def calculate_weight(current_height: float, next_height: float, step: float):
    """
    Calculate movement cost based on elevation change.
    Equal cost for uphill and downhill movements.

    Args:
        current_height: Height of current node
        next_height: Height of next node

    Returns:
        Cost of movement considering absolute height difference
    >>> calculate_weight(3, 7, step=3)
    5.0
    >>> calculate_weight(-7, 5, step=5)
    13.0
    """
    dh = abs(next_height - current_height)

    return math.sqrt(dh**2 + step**2)


def calculate_h_value(current: tuple[int, int], end: tuple[int, int]):
    return abs(current[0] - end[0]) + abs(current[1] - end[1])


def a_star_search(grid, step: int, start: tuple[int, int], end: tuple[int, int]):
    """
    A* Search Algorithm with equal costs for uphill and downhill movement.
    
    Args:
        grid: 2D list of heights for each cell
        src: Starting coordinates (row, col)
        dest: Destination coordinates (row, col)
    
    Returns:
        List of coordinates representing the path, or None if no path exists
    >>> grid = np.array([\
        [1.0, 1.2, 2.0, 3.0, 2.5],\
        [1.1, 1.8, 2.3, 2.5, 2.0],\
        [1.3, 2.0, 3.0, 2.0, 1.5],\
        [1.7, 2.2, 2.5, 1.5, 1.0],\
        [2.0, 2.5, 2.0, 1.2, 1.0]])
    >>> src = (0, 0)
    >>> dest = (4, 4)
    >>> a_star_search(grid, 1, src, dest)
    [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (4, 4)]
    >>> a_star_search(np.array([[1.0, 2.0, 3.0, 4.0], [1.5, 1.8, 2.5, 3.5], [2.0, 2.2, 2.0, 3.0], [2.5, 2.7, 2.3, 2.5]]), 1, (0, 0), (3, 3))
    [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)]
    >>> a_star_search([[10, 12, 15, 14, 11], [13, 18, 20, 19, 16], [14, 22, 25, 24, 20], [11, 15, 18, 17, 15], [10, 12, 14, 13, 10]], 1, (0,0),  (4,4))
    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (2, 3), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4)]
    """
    nodes = np.full((*grid.shape, 4), (math.inf, math.inf, -1, -1), "d, d, d, d")
    nodes[start] = (
        (f_start := calculate_h_value(start, end)),
        0,
        -1,
        -1,
    )  # f, g, parentx, parenty

    open_list = [(f_start, start)]
    with open("log.txt", "w", encoding="utf-8") as f:
        print(open_list, file=f)
    while open_list:
        if (result := a_star_next_step(open_list, nodes, end, grid, step)) is not None:
            return result
    return None


def a_star_next_step(open_list, nodes, end, grid, step):
    current_node = heappop(open_list)
    with open("log.txt", "w", encoding="utf-8") as f:
        print(current_node, file=f)
    if current_node == end:
        return trace_path(nodes[current_node], nodes)
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    neighbors = [
        (current_node[0] + a, current_node[1] + b)
        for a, b in directions
        if current_node[0] + a >= 0 and current_node[1] + b >= 0
    ]

    for neighbor in neighbors:
        tentative_g = nodes[current_node][1][1] + calculate_weight(
            grid[current_node], grid[neighbor], step
        )
        if tentative_g < nodes[neighbor][1][1]:
            nodes[neighbor] = (
                tentative_g + calculate_h_value(neighbor, end),
                tentative_g,
                *current_node,
            )
            if neighbor not in open_list:
                heappush(open_list, neighbor)
