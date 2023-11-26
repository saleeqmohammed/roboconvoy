#!/usr/bin/python3
import cv2
import tools.datamanagement as datamanagement
import numpy as np
import math
from pomdp.state_space_generator import get_states #type: ignore

state_matrix = None
#get state matrix from serialised file or otherwise
try:
    state_matrix =datamanagement.load_object("/home/saleeq/catkin_ws/src/roboconvoy/data/states/state_matrix_induvidual_agents.pickle")
except:
    state_matrix=get_states("data/states/new_map.pgm")
print(state_matrix)
"""
cv2.imshow("sm",state_matrix)
cv2.waitKey(0)
cv2.destroyAllWindows() 
"""
def euclidian_value(x1,y1,tupx2y2):
    return math.sqrt((x1-tupx2y2[0])**2+(y1-tupx2y2[1])**2)


def get_values(state_matrix,tgt_state):
    #initialize value matrix
    value_matrix = np.zeros_like(state_matrix)
    dims = state_matrix.shape
    n_x = dims[0]
    n_y = dims[1]
    for i in range(n_x):
        for j in range(n_y):
            if state_matrix[i,j]!=0:
                value_matrix[i,j]=-euclidian_value(i,j,tgt_state) #type: ignore
            else:
                value_matrix[i,j]=-10000 #type: ignore
    value_matrix[tgt_state[0],tgt_state[1]]=100 # type: ignore
    return value_matrix

tgt_state =(20,10)
value_matrix =get_values(state_matrix,tgt_state)