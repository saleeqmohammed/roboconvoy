import cv2
import numpy as np

# Load the image in black and white (0 - b&w, 1 - color).
image_path = '/mnt/data/PNG image.png'
image = cv2.imread(image_path, 0)

# Threshold the image to ensure it's binary
_, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

# Invert the image: black becomes white and white becomes black
binary_image = cv2.bitwise_not(binary_image)

# Find contours to estimate the line thickness
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Assume the first contour has a representative line thickness
_, _, _, line_thickness = cv2.boundingRect(contours[0])

# Create a grid matrix based on the line thickness
height, width = binary_image.shape
grid_height = height // line_thickness
grid_width = width // line_thickness

# Initialize grid matrix
grid_matrix = np.zeros((grid_height, grid_width), dtype=int)

# Fill the grid matrix
for i in range(grid_height):
    for j in range(grid_width):
        # Check the center of each grid cell
        y = i * line_thickness + line_thickness // 2
        x = j * line_thickness + line_thickness // 2
        if binary_image[y, x] == 0:  # Black
            grid_matrix[i, j] = 0
        else:  # White
            grid_matrix[i, j] = 1

grid_matrix
