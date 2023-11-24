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

# Example usage
matrix = [
    [0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

result = find_first_last_nonzero_indices(matrix)

if result is not None:
    print("First non-zero index:", result[0])
    print("Last non-zero index:", result[1])
else:
    print("No non-zero elements found in the matrix.")
import cv2
import numpy as np

# Assuming 'binary_array' is your binary NumPy array
binary_array = np.random.choice([0, 1], size=(100, 100))  # Replace this with your actual array

# Convert the binary array to an 8-bit unsigned integer array
image_array = binary_array.astype(np.uint8) * 255

# Convert the NumPy array to a CV2 image (assuming grayscale)
bw_image = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)

# Display the image using OpenCV (optional)
cv2.imshow("Converted Image", bw_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
