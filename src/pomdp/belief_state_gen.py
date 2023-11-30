from tokenize import String
import cv2
import numpy as np
import math
import tools.datamanagement as datamanagement
map_resolution = 0.05000000074505806
import matplotlib.pyplot as plt


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
    #print(n_cells_x)
    #print(n_cells_y)
    state_matrix = np.zeros((n_cells_x, n_cells_y))
    centers_dict = {}  # Dictionary to store centers as keys and state_matrix[cell_x, cell_y] as values

    pixels_x = n_cells_x * grid
    pixels_y = n_cells_y * grid
    padded_map = np.ones((pixels_y, pixels_x), dtype=np.uint8) * 255  # type: ignore
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
                centers_dict[(center_x*map_resolution, center_y*map_resolution)] = 1
                img_references[n_cell]=(center_x*map_resolution, center_y*map_resolution)
                #add labels
                label = f's{n_cell}'
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


def display_maps(result):
    if result is not None:
        # Display the original and modified images
        cv2.imshow("Original Image", cv2.imread(image_path, cv2.IMREAD_GRAYSCALE))
        cv2.imshow("Modified Image", result)
        # print(result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def get_states(map_image_path: String):  # type: ignore
    trimmed_image = trim_whitespace(map_image_path)
    state_matrix, centers_dict ,img_ref= state_matrix_generator(trimmed_image)
    state_matrix = state_matrix.T 
    state_matrix = state_matrix[1:-1,1:-1]
    return state_matrix, centers_dict,img_ref


image_path = "/home/saleeq/Desktop/new_map_planning_1.png"

""" state_matrix, centers_dict,img_ref = get_states(image_path)

# Print centers as a dictionary
print("Centers Dictionary:", centers_dict)
#we have to convert this to belief states normalize all probabilities
beliefstates =centers_dict#{key:value/sum(centers_dict.values()) for key,value in centers_dict.items()}
print(beliefstates)
cv2.waitKey(0)
cv2.destroyAllWindows()
datamanagement.save_object(beliefstates,"/home/saleeq/catkin_ws/src/roboconvoy/src/pomdp/beliefstates")
datamanagement.save_object(img_ref,"/home/saleeq/catkin_ws/src/roboconvoy/src/pomdp/beliefstate_reference")
datamanagement.save_object(state_matrix,"/home/saleeq/catkin_ws/src/roboconvoy/src/pomdp/availability_matrix") """
