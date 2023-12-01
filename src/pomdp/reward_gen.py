from tokenize import String
import cv2
import numpy as np
import math
import pomdp.belief_state_gen as beliefgen


floor_plan = "/home/saleeq/Desktop/new_map_planning_1.png"
state_matrix, centers_dict,belief_ref = beliefgen.get_states(floor_plan)

"""
        R(s,a)
        |S| x |A|
give a reward of 10 on moving to goal

"""
def get_neighbors(matrix, row_col):
    row =row_col[0]
    col =row_col[1]
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
def get_numbered(state_matrix):
    cum=0
    for i in range(state_matrix.shape[0]):
        for j in range(state_matrix.shape[1]):
            if state_matrix[i,j]:
                cum+=state_matrix[i,j]
                state_matrix[i,j]=cum
    return state_matrix

floor_plan = "/home/saleeq/Desktop/new_map_planning_1.png"
state_matrix, centers_dict,belief_ref = beliefgen.get_states(floor_plan)
#print(belief_ref)
#print(state_matrix)
state_action_pairs = generate_state_action_pairs(arr)#state_matrix)
#print(state_action_pairs)
T =getTransitions(state_action_pairs)

#print(T.shape)
Tr = np.zeros((len(belief_ref),4,len(belief_ref)))
index_state_matrix =get_numbered(state_matrix)
print(index_state_matrix)

#print(Tr)

#print(len(belief_ref))
belief_state_indeces ={}
for belief_state in belief_ref.keys():
    for i in range(state_matrix.shape[0]):
        for j in range(state_matrix.shape[1]):
            if belief_state == state_matrix[i,j]-1:
                belief_state_indeces[belief_state]=(i,j)
#print(belief_state_indeces)
belief_state_neighbours={}
for belief_state in belief_ref.keys():
    belief_state_neighbours[belief_state]=get_neighbors(index_state_matrix,belief_state_indeces[belief_state])
print(belief_state_neighbours)
#for each action, map the belief state to itself with probability of 1 if there is a blocked action in neighbours
# up row1
#down row2
#right row3
#left row4
actions=["up","down","right","left"]
def get_rewards(goal_belief_state):
    #Define the reward matrix
    # |S| x |A|
    #1st column Up
    #2nd column down
    #3rd column right
    #4th column left

    R = np.zeros((belief_ref.keys(),len(actions)))
    #find the neighbours of goal state and assign +10 
    # to the action to complete mission 😎
    goal_state_neighbours = belief_state_neighbours[goal_belief_state]
    goal_state_indeces = belief_state_indeces[target_belief_state]
    #if "going up from the goal" state is unblocked add +10 reward to the down state for action up
    if state_matrix[goal_state_indeces[0]-1,goal_state_indeces[1]]
    