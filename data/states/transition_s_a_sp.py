from tokenize import String
import cv2
import numpy as np
import math
import datamanagement
map_resolution = 0.05000000074505806
import matplotlib.pyplot as plt

successful_probability =0.88
opposite_probability =0
def find_first_last_nonzero_indices(matrix):
    # Convert the matrix to a NumPy array
    matrix = np.array(matrix)

    # Find the indices of non-zero elements
    non_zero_indices = np.nonzero(matrix)

    if len(non_zero_indices[0]) == 0:
        # If there are no non-zero elements, return None
        return None
    else:
        # Find the first and last non-zero indices
        first_nonzero = (non_zero_indices[0][0], non_zero_indices[1][0])
        last_nonzero = (non_zero_indices[0][-1], non_zero_indices[1][-1])

        return first_nonzero, last_nonzero


def trim_whitespace(image_path):
    # Read the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    #cv2.imshow("Original Image", cv2.imread(image_path, cv2.IMREAD_GRAYSCALE))
    img_matrix = np.array(img)
    img_matrix = img_matrix <= 0

    bin_image = img_matrix.astype(int)
    # print(bin_image)
    non_zero_bounding = find_first_last_nonzero_indices(bin_image)
    top_left = non_zero_bounding[0]  # type:ignore
    bottom_right = non_zero_bounding[1]  # type:ignore
    x = top_left[0]
    y = top_left[1]
    x2 = bottom_right[0]
    y2 = bottom_right[1]

    # print(bin_image)
    cv2.imshow("Trimmed Image", img[x:x2, y:y2])
    return img[x:x2, y:y2]


def calculate_grid_size(img_map):
    i = 0
    while img_map[i, i] == 0:
        i = i + 1

    return i


def state_matrix_generator(map_img):
    grid = 16
    map_dim = map_img.shape
    x_dim = map_dim[1]
    y_dim = map_dim[0]
    n_cells_x = math.ceil(x_dim / grid)
    n_cells_y = math.ceil(y_dim / grid)
    print(n_cells_x)
    print(n_cells_y)
    state_matrix = np.zeros((n_cells_x, n_cells_y))
    centers_dict = {}  # Dictionary to store centers as keys and state_matrix[cell_x, cell_y] as values

    pixels_x = n_cells_x * grid
    pixels_y = n_cells_y * grid
    padded_map = np.zeros((pixels_y, pixels_x), dtype=np.uint8) # type: ignore
    padded_map[:y_dim, :x_dim] = map_img
    image_bgr = cv2.cvtColor(padded_map, cv2.COLOR_GRAY2BGR)
    n_cell =0
    img_references ={}
    for cell_y in range(1,n_cells_y-1):
        for cell_x in range(1,n_cells_x-1):
            start_x = cell_x * grid
            start_y = cell_y * grid
            end_x = (cell_x + 1) * grid
            end_y = (cell_y + 1) * grid

            center_x = (start_x + end_x) // 2
            center_y = (start_y + end_y) // 2
            

            if np.sum(padded_map[start_y:end_y, start_x:end_x]) > (255 * grid ** 2 - 1) * 0.99:
                # allowed cells
                cv2.rectangle(image_bgr, (start_x, start_y), (end_x, end_y), (0, 100, 0), -1)
                cv2.circle(image_bgr, (center_x, center_y), 2, (0, 0, 255), -1)  # Add a dot at the center
                state_matrix[cell_x, cell_y] = 1
                centers_dict[(center_x, center_y)] = 1
                img_references[n_cell]=(center_x, center_y)
                #add labels
                label = '<'
                n_cell+=1
                cv2.putText(image_bgr, label, (center_x - 5, center_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (255, 0, 0), 1, cv2.LINE_AA)
            else:
                cv2.rectangle(image_bgr, (start_x, start_y), (end_x, end_y), (0, 0, 100), -1)
                #just don't add extra states
                #centers_dict[(center_x*map_resolution, center_y*map_resolution)] = 0

    
    cv2.imshow("Grid", image_bgr)
    cv2.imwrite("/home/saleeq/Desktop/grid_map.png", image_bgr)
    state_matrix = state_matrix
    
    return state_matrix, centers_dict, img_references


def get_states(map_image_path: String):  # type: ignore
    trimmed_image = trim_whitespace(map_image_path)
    state_matrix, centers_dict ,img_ref= state_matrix_generator(trimmed_image)
    return state_matrix, centers_dict,img_ref


image_path = "/home/saleeq/Desktop/new_map_planning_1.png"

state_matrix, centers_dict,img_ref = get_states(image_path)
#cv2.waitKey(0)
cv2.destroyAllWindows
state_matrix = state_matrix[1:-1,1:-1]
state_matrix=state_matrix.T
print(state_matrix)
print(len(centers_dict))
print(state_matrix.size)



import numpy as np
""" 
def create_directional_dictionary(arr, direction):
    result_dict = {}
    rows, cols = arr.shape

    for i in range(rows):
        for j in range(cols):
            if arr[i, j] == 1:
                # Initialize neighbor_indices to None
                neighbor_indices = None

                # Determine the neighboring indices based on the direction
                if direction == 'up':
                    neighbor_indices_up = (i-1, j) if i > 0 else None
                    neighbor_indices_down =(i+1, j) if i < rows - 1 else None
                    neighbor_indices_left =(i, j-1) if j > 0 else None
                    neighbor_indices_right =(i, j-1) if j > 0 else None
                    #add to the list in the order same direction,opposite direction, perpendicular1, perpendicular2
                    neighbor_indices=[neighbor_indices_up,neighbor_indices_down,neighbor_indices_right,neighbor_indices_left]
                elif direction == 'down':
                    neighbor_indices = (i+1, j) if i < rows - 1 else None
                elif direction == 'left':
                    neighbor_indices = (i, j-1) if j > 0 else None
                elif direction == 'right':
                    neighbor_indices = (i, j-1) if j > 0 else None

                # Check if the neighboring entry exists and assign the value accordingly
                #same_direction 0.8
                if neighbor_indices[0] is not None:
                    neighbor_value = arr[neighbor_indices]
                    result_dict[(i, j)] = (0.8,neighbor_indices) if neighbor_value == 1 else (1,(i,j))
                #opposite_direction 0.04
                if neighbor_indices[1] is not None:
                    neighbor_value = arr[neighbor_indices]
                    result_dict[(i, j)] = (0.04,neighbor_indices) if neighbor_value == 1 else (1,(i,j))
                    #perpendicular 1 0.08
                if neighbor_indices[2] is not None:
                    neighbor_value = arr[neighbor_indices]
                    result_dict[(i, j)] = (0.8,neighbor_indices) if neighbor_value == 1 else (1,(i,j))
                    #perpendicular 2 0.08
                if neighbor_indices[3] is not None:
                    neighbor_value = arr[neighbor_indices]
                    result_dict[(i, j)] = (0.8,neighbor_indices) if neighbor_value == 1 else (1,(i,j))

    return result_dict 

# Example usage:
# Assuming your 2D array is named 'my_array'
my_array = state_matrix

#probability of moving up in every state
result_up = create_directional_dictionary(my_array, 'up')
#probability of moving down in every state
result_down = create_directional_dictionary(my_array, 'down')
#probability of moving up in every state
result_left = create_directional_dictionary(my_array, 'left')
result_right = create_directional_dictionary(my_array, 'right')
"""
""" 
print("Up:", result_up)
print("Down:", result_down)
print("Left:", result_left)
print("Right:", result_right)
action_prob={'up':result_up,'down':result_down,'left':result_left,'right':result_right}
cT = np.ones((n_states,n_actions,n_states))
for s in range(n_state):
    for a in range(n_actions):
        for s_p in range(n_states):
            cT[s][a][s_p] =  """
import numpy as np

def create_directional_dictionary(arr, direction):
    result_dict = {}
    rows, cols = arr.shape

    for i in range(rows):
        for j in range(cols):
            if arr[i, j] == 1:
                # Initialize neighbor_indices and weights based on the direction
                if direction == 'up':
                    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                    weights = [0.8, 0.04, 0.08, 0.08]
                elif direction == 'down':
                    neighbors = [(i+1, j)]
                    weights = [0.8]
                elif direction == 'left':
                    neighbors = [(i, j-1)]
                    weights = [0.8]
                elif direction == 'right':
                    neighbors = [(i, j+1)]
                    weights = [0.8]

                # Check if the neighboring entry exists and assign the value accordingly
                for neighbor, weight in zip(neighbors, weights):
                    if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                        neighbor_value = arr[neighbor]
                        result_dict[(i, j)] = (weight, neighbor) if neighbor_value == 1 else (1, (i, j))

    return result_dict

# Example usage:
arr = np.array([[1, 0, 1],
                [0, 1, 0],
                [1, 0, 1]])

directions = ['up', 'down', 'left', 'right']

for direction in directions:
    result = create_directional_dictionary(arr, direction)
    print(f"{direction}: {result}")
