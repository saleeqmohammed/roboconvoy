#!/usr/bin/python3


import cv2
import tools.datamanagement as datamanage
import numpy as np
import math
from pomdp.state_space_generator import get_states #type: ignore
from matplotlib import pyplot as plt
from copy import deepcopy
state_matrix = None
#get state matrix from serialised file or otherwise
try:
    state_matrix =datamanage.load_object("/home/saleeq/catkin_ws/src/roboconvoy/data/states/state_matrix_induvidual_agents.pickle")
except:
    state_matrix=get_states("data/states/new_map.pgm")

#to match real world take transpose
state_matrix = state_matrix.T
#to generate states we need all possible coordinates
dim_states = state_matrix.shape
print(f'diminsion of states: {dim_states}')
""" cv2.imshow("state matrix",state_matrix)
cv2.waitKey(0)
cv2.destroyAllWindows()
 """
available_gridcells = []
for x in range(dim_states[0]):
    for y in range(dim_states[1]):
        if state_matrix[x,y]:
            available_gridcells.append((x,y))
#print(available_gridcells)


robot_1_states = deepcopy(available_gridcells)
robot_2_states = deepcopy(available_gridcells)


# Define the size of the grid
x_size = dim_states[0]
y_size = dim_states[1]

# Create a figure and axis
fig, ax = plt.subplots()

# Draw vertical lines for the grid
for i in range(x_size + 1):
    ax.axvline(i, color='gray', linestyle='--', linewidth=0.5)

# Draw horizontal lines for the grid
for i in range(y_size + 1):
    ax.axhline(i, color='gray', linestyle='--', linewidth=0.5)

# Set axis limits
ax.set_xlim(0, x_size)
ax.set_ylim(0, y_size)

# Set axis labels
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')

# Set the aspect ratio to be equal, so the grid cells are square
ax.set_aspect('equal')

# Show the plot
plt.show()
