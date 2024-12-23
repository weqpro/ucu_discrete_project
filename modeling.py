import numpy as np
from matplotlib import pyplot as plt
import trimesh
import scipy.spatial
import matplotlib.colors as mcolors

START = (1, 3)
END = (2, 5)
STEP = 1


def find_connecting_points(
    x1: float, x2: float, y1: float, y2: float, strength: float = 0.15
) -> tuple[float, float]:
    """
    finds the to points in between vertices to smooth out the trasition

    :param x1: the x of first point < x2
    :param x2: the x of second point > x1
    :param y1: the y of first point
    :param y2: the y of second point
    """

    def linear_interpolation():
        return lambda x: y1 + ((y2 - y1) * (x - x1)) / (x2 - x1)

    y = linear_interpolation()
    smooth_y1 = (y(0.20 * (x2 - x1) + x1) - y1) - ((y2 - y1) * strength) + y1
    smooth_y2 = (y(0.80 * (x2 - x1) + x1) - y1) + ((y2 - y1) * strength) + y1

    return smooth_y1, smooth_y2


def create_terrain_colormap():
    """
    Create a custom colormap for terrain visualization.

    The colormap mimics natural terrain colors:
    - Dark blue/navy for lowest elevations (water/deep valleys)
    - Green for low to mid elevations (lowlands, forests)
    - Brown/tan for higher elevations (hills)
    - White for peaks (snow-capped mountains)

    Returns:
    - matplotlib colormap
    """
    # Define colors from low to high elevation
    colors = [
        "#62d96d",
        "#38c40e",
        "#44ad10",
        "#008000",  # Dark green (forests)
        "#8B4513",  # Saddle brown (hills)
        "#A0522D",  # Sienna (higher hills)
        "#D2691E",  # Chocolate (mountain slopes)
    ]

    # Create a color map
    return mcolors.LinearSegmentedColormap.from_list("terrain_colormap", colors, N=256)


def elevation_grid_to_mesh(elevation_grid, colormap):
    """
    Convert elevation grid to a trimesh triangulated surface with color information.

    This function does several key things:
    1. Creates vertex coordinates from the grid
    2. Triangulates the surface using Delaunay triangulation
    3. Applies a color map to the vertices based on their elevation

    Parameters:
    - elevation_grid: 2D numpy array of elevation values
    - colormap: Matplotlib colormap for terrain coloration

    Returns:
    - trimesh.Trimesh object representing the colored terrain surface
    """
    # Get grid dimensions
    height, width = elevation_grid.shape

    # Normalize elevation for color mapping
    elevation_normalized = (elevation_grid - elevation_grid.min()) / (
        elevation_grid.max() - elevation_grid.min()
    )

    # Create vertex coordinates
    x = np.linspace(0, width - 1, width)
    y = np.linspace(0, height - 1, height)
    X, Y = np.meshgrid(x, y)

    # Flatten coordinates and elevation
    vertices = np.column_stack([X.ravel(), Y.ravel(), elevation_grid.ravel()])

    # Create faces using Delaunay triangulation
    faces = scipy.spatial.Delaunay(vertices[:, :2]).simplices

    # Map colors to vertices based on normalized elevation
    vertex_colors = colormap(elevation_normalized.ravel())[:, :3] * 255

    # Create trimesh object with color information
    mesh = trimesh.Trimesh(
        vertices=vertices, faces=faces, vertex_colors=vertex_colors.astype(np.uint8)
    )

    return mesh


def draw_point_on_grid_mesh(grid_mesh, x, y, color=[255, 0, 0], radius=0.1):
    """
    Draw a point on an existing grid mesh at specified (x, y) coordinates,
    finding elevation from the mesh vertices.

    Parameters:
    - grid_mesh: Existing Trimesh object of the grid
    - x: x-coordinate of the point
    - y: y-coordinate of the point
    - color: RGB color of the point (default is red)
    - radius: Size of the point (default is 0.1)

    Returns:
    - A new Trimesh object with the point added
    """
    # Find the z elevation by interpolating from mesh vertices
    # First, find the closest vertices
    vertices = grid_mesh.vertices

    # Calculate distances to all vertices
    distances = np.sqrt((vertices[:, 0] - x) ** 2 + (vertices[:, 1] - y) ** 2)

    # Find indices of the 4 closest vertices
    closest_indices = np.argsort(distances)[:4]
    closest_vertices = vertices[closest_indices]

    # Perform inverse distance weighted interpolation
    weights = 1.0 / (distances[closest_indices] + 1e-10)
    weights /= weights.sum()

    # Interpolate z coordinate
    z = np.sum(closest_vertices[:, 2] * weights)

    # Create a point sphere
    point_sphere = trimesh.creation.icosphere(radius=radius)

    # Translate the point sphere to the specified location
    point_sphere.apply_translation([x, y, z])

    # Color the point
    point_sphere.visual.face_colors = color

    # Combine the original mesh with the point
    combined_mesh = trimesh.util.concatenate([grid_mesh, point_sphere])

    return combined_mesh


def export_elevation_to_glb(grid_mesh, output_path="terrain.glb"):
    """
    Export an elevation grid to a .glb file with color information.

    Parameters:
    - elevation_grid: 2D numpy array of elevation values
    - output_path: Path to save the .glb file
    """
    try:
        grid_mesh.export(output_path)

        print(f"Colored elevation grid exported successfully to {output_path}")
    except Exception as e:
        print(f"Error exporting elevation grid: {e}")


def smooth_grid(grid):
    """
    Smooths a 2D grid by adding intermediate points between adjacent elements in each row.

    This function takes a 2D array (or list of lists), and for each row, it calculates two
    additional points between every pair of adjacent elements. The resulting grid has
    smoothed rows with additional points, and all rows are padded with zeros to match the
    length of the longest row.

    Parameters
    ----------
    grid : list[list[float]] or numpy.ndarray
        The input 2D array or grid. Each row represents a sequence of values (e.g., coordinates or data points).
        Rows can have different lengths, but the function ensures uniformity in the output.

    Returns
    -------
    numpy.ndarray
        A smoothed 2D array where each row contains the original points and newly added
        intermediate points. All rows are padded with zeros to ensure uniform row length.
    """

    smoothed_grid = []
    row_min = min({min(row) for row in grid})

    for row in grid:
        smoothed_row = []
        smoothed_row.append(row_min)

        for i in range(len(row) - 1):
            x1, x2 = i, i + 1
            y1, y2 = row[i], row[i + 1]
            new_y1, new_y2 = find_connecting_points(x1, x2, y1, y2)
            smoothed_row.append(row[i])
            smoothed_row.extend([new_y1, new_y2])

        smoothed_row.append(row[-1])

        smoothed_row.append(row_min)

        smoothed_grid.append(smoothed_row)

    max_length = max(len(row) for row in smoothed_grid)
    smoothed_grid = np.array(
        [np.pad(row, (0, max_length - len(row))) for row in smoothed_grid]
    )

    return smoothed_grid


def main():
    grid = np.loadtxt(open("test.csv", "rb"), delimiter=",")

    from a_star import a_star_search_with_height

    path = a_star_search_with_height(grid.tolist(), STEP, START, END)

    colormap = create_terrain_colormap()

    smth = elevation_grid_to_mesh(smooth_grid(smooth_grid(grid).T).T, colormap)
    if path is not None:
        for point in path:
            smth = draw_point_on_grid_mesh(smth, *point, color=[66, 135, 245])

    export_elevation_to_glb(smth, output_path="www/root/sample_terrain2.glb")


if __name__ == "__main__":
    main()
