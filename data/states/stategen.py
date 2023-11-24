import cv2
import numpy as np
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
    print(bin_image)
    non_zero_bounding = find_first_last_nonzero_indices(bin_image)
    top_left = non_zero_bounding[0]
    bottom_right=non_zero_bounding[1]
    x=top_left[0]
    y=top_left[1]
    x2 = bottom_right[0]
    y2 = bottom_right[1]
    print(x)
    print(y)
    
    #print(bin_image)
    return img[x:x2,y:y2]
# Example usage
image_path = "/home/saleeq/catkin_ws/src/roboconvoy/data/states/new_map.pgm"
result = trim_whitespace(image_path)

if result is not None:
    # Display the original and modified images
    cv2.imshow("Original Image", cv2.imread(image_path, cv2.IMREAD_GRAYSCALE))
    cv2.imshow("Modified Image", result)
    #print(result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
