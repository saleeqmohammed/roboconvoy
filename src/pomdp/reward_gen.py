from tokenize import String
import cv2
import numpy as np
import math
import pomdp.belief_state_gen as beliefgen


floor_plan = "/home/saleeq/Desktop/new_map_planning_1.png"
state_matrix, centers_dict,belief_ref = beliefgen.get_states(floor_plan)


def generate_state_action_pairs(state_matrix):

    directions = ['up', 'down', 'left', 'right']
    state_action_pairs=[]
    for direction in directions:
        state_action_pairs.append(create_directional_dictionary(arr, direction))
        #print(f"{direction}: {state_action_pairs}")
    return state_action_pairs


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
index_state_matrix = get_numbered(state_matrix)

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
#print(belief_state_neighbours)
#for each action, map the belief state to itself with probability of 1 if there is a blocked action in neighbours
# up row1
#down row2
#right row3
#left row4


actions=["up","down","right","left"]
"""
        R(s,a)
        |S| x |A|
give a reward of 10 on moving to goal

"""


def get_rewards(goal_belief_state):
    #Define the reward matrix
    # |S| x |A|
    #0 column Up
    #1column down
    #2 column right
    #3 column left

    #initialize with small negaive penalty for movement to avoid unnecesary moves
    R = np.ones((len(belief_ref.keys()),len(actions)))*-0.1
    #find the neighbours of goal state and assign +10 
    # to the action to complete mission 😎
    goal_state_neighbours = belief_state_neighbours[goal_belief_state]
    goal_state_indeces = belief_state_indeces[goal_belief_state]
    # 🧠if "going up from the goal" state is unblocked add +10 reward to the state above for action down
    if state_matrix[goal_state_indeces[0]-1,goal_state_indeces[1]]:
        R[goal_state_indeces[0]-1,goal_state_indeces[1]][1]=10
    #if going down from goal state is unblocked add +10 for the state below for action up
    if state_matrix[goal_state_indeces[0]+1,goal_state_indeces[1]]:
        R[goal_state_indeces[0]+1,goal_state_indeces[1]][0]=10
    #if going right from goal state is unblocked add +10 for the to the right for action left
    if state_matrix[goal_state_indeces[0],goal_state_indeces[1]+1]:
        R[goal_state_indeces[0],goal_state_indeces[1]+1][3]=10
        #if going left from goal state is unblocked add +10 for the to the left for action right
    if state_matrix[goal_state_indeces[0],goal_state_indeces[1]-1]:
        R[goal_state_indeces[0],goal_state_indeces[1]-1][3]=10

    #Put a very high negative penalty for blocked states 
    negative_state_indeces =[]
    for i in range(state_matrix.shape[0]):
        for j in range(state_matrix.shape[1]):
            if not state_matrix[i,j]:
                negative_state_indeces.append((i,j))
    negative_state_neighbours={}
    for negative_state_idx in negative_state_indeces:
            negative_state_neighbours[negative_state_idx] = get_neighbors(state_matrix,negative_idx)
            # 🧠if "going up from the negative" state is unblocked add +10 reward to the state above for action down
            if state_matrix[negative_state_idx[0]-1,negative_state_idx[1]]:
                R[negative_state_idx[0]-1,negative_state_idx[1]][1]=-10
            #if going down from negative state is unblocked add +10 for the state below for action up
            if state_matrix[negative_state_idx[0]+1,negative_state_idx[1]]:
                R[negative_state_idx[0]+1,negative_state_idx[1]][0]=-10
            #if going right from negative state is unblocked add +10 for the to the right for action left
            if state_matrix[negative_state_idx[0],negative_state_idx[1]+1]:
                R[negative_state_idx[0],negative_state_idx[1]+1][3]=-10
                #if going left from negative state is unblocked add +10 for the to the left for action right
            if state_matrix[negative_state_idx[0],negative_state_idx[1]-1]:
                R[negative_state_idx[0],negative_state_idx[1]-1][3]=-10
    return R


R =get_rewards(2)
