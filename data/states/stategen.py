from tokenize import String
import cv2
import numpy as np
import math
import datamanagement
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
    cv2.imshow("Original Image", cv2.imread(image_path, cv2.IMREAD_GRAYSCALE))
    img_matrix = np.array(img)
    img_matrix = img_matrix<=0

    bin_image = img_matrix.astype(int)
    #print(bin_image)
    non_zero_bounding = find_first_last_nonzero_indices(bin_image)
    top_left = non_zero_bounding[0] #type:ignore
    bottom_right=non_zero_bounding[1] #type:ignore
    x=top_left[0]
    y=top_left[1]
    x2 = bottom_right[0]
    y2 = bottom_right[1]
    
    #print(bin_image)
    return img[x:x2,y:y2]
# Example usage
def calculate_grid_size(img_map):
    i=0
    while img_map[i,i]==0:
        i = i+1

    return i

def state_matrix_generator(map_img):
    grid= calculate_grid_size(map_img)
    map_dim = map_img.shape
    x_dim =map_dim[1]
    y_dim =map_dim[0]
    n_cells_x = math.ceil(x_dim/grid)
    n_cells_y = math.ceil(y_dim/grid)
    print(n_cells_x)
    print(n_cells_y)
    state_matrix =np.zeros((n_cells_x,n_cells_y))
    #create a matrix that is the multiple of grid
    pixels_x = n_cells_x*grid
    pixels_y = n_cells_y*grid
    padded_map = np.ones((pixels_y,pixels_x), dtype=np.uint8) * 255 # type: ignore
    padded_map[:y_dim,:x_dim] = map_img
    image_bgr = cv2.cvtColor(padded_map, cv2.COLOR_GRAY2BGR)
    for cell_y in range(n_cells_y):
        for cell_x in range(n_cells_x):
            start_x =cell_x*grid
            start_y =cell_y*grid
            end_x =(cell_x+1)*grid
            end_y =(cell_y+1)*grid
            if np.sum(padded_map[start_y:end_y,start_x:end_x]) >(255*grid**2 -1):
                #allowed cells
                cv2.rectangle(image_bgr,(start_x,start_y),(end_x,end_y),(0,100,0),1)
                state_matrix[cell_x,cell_y]=1
            else:
                #cv2.rectangle(image_bgr,(start_x,start_y),(end_x,end_y),(0,0,100),-1)
                #no need to do anything unless plotting rectangles since initialized with 0s.
                pass
    
    # cv2.imshow("grid",image_bgr)
    
    #cv2.imwrite("/home/saleeq/catkin_ws/src/roboconvoy/data/states/grid_map.bmp",image_bgr)
    return state_matrix

image_path = "/home/saleeq/catkin_ws/src/roboconvoy/data/states/new_map.pgm"
result = trim_whitespace(image_path)
state_matrix =state_matrix_generator(result)
datamanagement.save_object(state_matrix,"/home/saleeq/catkin_ws/src/roboconvoy/data/states/state_matrix_induvidual_agents")

if result is not None:
    # Display the original and modified images 
    cv2.imshow("Original Image", cv2.imread(image_path, cv2.IMREAD_GRAYSCALE))
    cv2.imshow("Modified Image", result)
    #print(result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def get_states(map_image_path: String): # type: ignore
    trimmed_image = trim_whitespace(map_image_path)
    state_matrix =state_matrix_generator(trimmed_image)
    return state_matrix
