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
    """
    rows, cols = len(grid), len(grid[0])
    if not (is_valid(src[0], src[1], rows, cols) and
            is_valid(dest[0], dest[1], rows, cols)):
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
        'h': calculate_h_value(start_row, start_col, dest),
        'f': calculate_h_value(start_row, start_col, dest),
        'parent': None
    }
    heappush(open_list, (0, src))
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1)
    ]
    
    while open_list:
        _, current = heappop(open_list)
        row, col = current
        
        if (row, col) == dest:
            return trace_path(cell_details, dest)
            
        closed_list[row][col] = True
        for dy, dx in directions:
            new_row, new_col = row + dy, col + dx
            
            if not is_valid(new_row, new_col, rows, cols):
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
            h_new = calculate_h_value(new_row, new_col, dest)
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
