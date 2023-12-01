def get_neighbors(matrix, row, col):
    neighbors = []
    num_rows, num_cols = len(matrix), len(matrix[0])

    # Define the relative positions of neighbors (including diagonals)
    directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]

    for i, j in directions:
        new_row, new_col = row + i, col + j
        # Check if the new position is within the bounds of the matrix
        if 0 <= new_row < num_rows and 0 <= new_col < num_cols:
            neighbors.append((new_row, new_col))

    return neighbors

# Example usage:
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

index_row, index_col = 1, 1  # Example index

neighbors = get_neighbors(matrix, index_row, index_col)
print(f"Neighbors of index ({index_row}, {index_col}): {neighbors}")
