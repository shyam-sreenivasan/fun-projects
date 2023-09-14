import sys

# Constants
WALL = '#'
START = 'S'
TARGET = 'T'

# Directions for neighbors
DIRECTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]

def parse_maze_to_matrix(maze_str):
    maze = maze_str.strip().split("\n")
    return [list(row) for row in maze], len(maze), len(maze[0])

def is_valid_cell(matrix, visited, row, col):
    return 0 <= row < total_rows and 0 <= col < total_cols \
           and matrix[row][col] != WALL and not visited[row][col]

def visit(matrix, row, col, visited, depth=0, memo={}):
    key = f"{row}{col}"
    if key in memo and matrix[row][col] != TARGET:
        return memo[key]
    
    memo[key] = None
    visited[row][col] = True
    if matrix[row][col] == TARGET:
        memo[key] = (True, [(row, col)], depth)
        visited[row][col] = False
        return memo[key]

    found_paths = []
    depths = []
    for dr, dc in DIRECTIONS:
        next_row, next_col = row + dr, col + dc
        if is_valid_cell(matrix, visited, next_row, next_col):
            found, pth, max_depth = visit(matrix, next_row, next_col, visited, depth=depth+1)
            if found:
                found_paths.append([(row, col)] + pth)
                depths.append(max_depth)
                

    visited[row][col] = False

    if found_paths:
        min_depth_idx = depths.index(min(depths))
        memo[key] = (
            True,
            found_paths[min_depth_idx],
            depths[min_depth_idx]
        )
        return memo[key]
    
    memo[key] = (False, None, None)
    return memo[key]

# def visit(matrix, row, col, visited, path):
#     visited[row][col] = True
#     path.append((row, col))

#     if matrix[row][col] == TARGET:
#         temp = path.copy()
#         path.pop()
#         visited[row][col] = False
#         return True, temp

#     found_paths = []
#     for dr, dc in DIRECTIONS:
#         next_row, next_col = row + dr, col + dc
#         if is_valid_cell(matrix, visited, next_row, next_col):
#             found, pth = visit(matrix, next_row, next_col, visited, path)
#             if found:
#                 found_paths.append(pth)

#     visited[row][col] = False
#     path.pop()

#     if found_paths:
#         min_path = min(found_paths, key=len)
#         return True, min_path

#     return False, path

def find_start_cell(matrix):
    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell == START:
                return row_idx, col_idx
    return None, None

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python maze_solver.py <maze>")
        sys.exit(1)

    maze = sys.argv[1]
    matrix, total_rows, total_cols = parse_maze_to_matrix(maze)
    visited = [[False] * total_cols for _ in range(total_rows)]

    start_row, start_col = find_start_cell(matrix)
    if start_row is not None and start_col is not None:
        path = []
        target_found, path, max_depth = visit(matrix, start_row, start_col, visited, depth=0)
        print("==============================")
        if target_found:
            print("Found path:", path)
            print("Path length:", len(path), max_depth)
        else:
            print("No path found.")
    else:
        print("No start position found.")
