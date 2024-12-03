"""main module"""
import argparse
import a_star

def main():
    """main module function"""
    parser = argparse.ArgumentParser(description="A* Path Finding Script")
    parser.add_argument("filepath", type=str, help="Path to the grid file")
    parser.add_argument("--src", type=int, nargs=2,
                        metavar=('SRC_X', 'SRC_Y'),
                        help="Source coordinates (x y)")
    parser.add_argument("--dest", type=int, nargs=2,
                        metavar=('DEST_X', 'DEST_Y'),
                        help="Destination coordinates (x y)")
    args = parser.parse_args()
    src = tuple(args.src)
    dest = tuple(args.dest)
    print(f"File path provided: {args.filepath}")
    print(f"Source coordinates: {src}")
    print(f"Destination coordinates: {dest}")
    grid = []
    try:
        with open(args.filepath, 'r', encoding='utf-8') as file:
            for line in file:
                row = []
                chars = line.strip().split()
                for char in chars:
                    row.append(float(char))
                grid.append(row)
    except FileNotFoundError:
        print("Error: File not found. Please provide a valid file path.")
        return
    path = a_star.a_star_search_with_height(grid, src, dest)
    if path:
        print("Path found:", path)
    else:
        print("No path found!")

if __name__ == '__main__':
    main()
