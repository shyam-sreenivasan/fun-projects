DIRECTIONS = [
    (-1, 2),
    (-1, -2),
    (-2, 1),
    (-2, -1),
    (1, 2),
    (1, -2),
    (2, 1),
    (2, -1)
]
def get_squares(n):
    squares = []
    for _ in range(n):
        row = [False]*n
        squares.append(row)
    return squares

def get_next_positions(row, col):
    return (
        (row-1, col-2), 
        (row-2, col-1), 
        (row+2, col-1), 
        (row+1, col-2),
        (row-1, col+2),
        (row-2, col+1),
        (row+1, col+2),
        (row+2, col+1)
        )

def valid_position(pos, dimen):
    return 0 <= pos[0] < dimen and 0 <= pos[1] < dimen

def is_valid_position(row, col, dimen, squares):
    return (0 <= row < dimen and 0 <= col < dimen) and not squares[row][col]

def all_squares_visited(squares, path):
    return len(path) == (len(squares)*len(squares))

def visit(squares, row_pos, col_pos, depth=1): 
    squares[row_pos][col_pos] = True
    pos = f"{row_pos}{col_pos}"

    if depth == (dimen*dimen):
        return True, [pos]
    
    for dr, dc in DIRECTIONS:
        next_row = row_pos + dr
        next_col = col_pos + dc
        if is_valid_position(next_row, next_col, dimen, squares):
            path_found, pth = visit(squares, next_row, next_col, depth=depth+1)
            if path_found:
                return True, [pos] + pth

    squares[row_pos][col_pos] = False
    return False, None

# def visit(squares, row_pos, col_pos, path=[]): 
#     pos = f"{row_pos}{col_pos}"
#     path.append(pos)
#     print("Path: ", path)

#     squares[row_pos][col_pos] = True
#     next_positions = get_next_positions(row_pos, col_pos)
#     valid_positions = [pos for pos in next_positions if valid_position(pos, len(squares))]
    
#     # consider the valid positions that are not already in the path
#     # and yet to be visited
#     valid_positions = [p for p in valid_positions if f"{p[0]}{p[1]}" not in path]

#     if all_squares_visited(squares, path):
#         print(f"All squares visited {path}")
#         return True
    
#     for vp in valid_positions:
#         path_found = visit(squares, vp[0], vp[1], path=path)
#         if path_found:
#             return True
        
#     # removing current position from path as it leads to a dead end
#     path.pop()

#     # setting to False as there is no valid path from this square
#     # and hence keep it open for visiting from other routes.
#     squares[row_pos][col_pos] = False
#     return False
    

if __name__ == "__main__":
    import sys
    dimen = int(sys.argv[1])
    for i in range(dimen):
        squares = get_squares(dimen)
        for j in range(dimen):
            print(f"Starting from {i}{j}")
            path_found, path = visit(squares, i,j)
            if path_found:
                print(f"Path found from {i}{j}: {path}")
                sys.exit(0)
    print("No path found from any position")