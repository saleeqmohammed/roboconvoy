from tokenize import String
import cv2
import numpy as np
import math
import pomdp.belief_state_gen as beliefgen

def create_directional_dictionary(arr, direction):
    result_dict = {}
    rows, cols = arr.shape

    for i in range(rows):
        for j in range(cols):
            if arr[i, j] == 1:
                # Initialize neighbor_indices and weights based on the direction
                if direction == 'up':
                                #left       #right    #up    #down
                    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                               #p1  #p2   #Same #opp
                    weights = [0.08, 0.08, 0.8, 0.04]
                elif direction == 'down':
                                #left       #right    #up    #down
                    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                                #p2    #p1 #opp #same
                    weights = [0.08, 0.08, 0.04, 0.8]
                elif direction == 'left':
                                #left       #right    #up    #down
                    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                    weights = [0.8, 0.04, 0.08, 0.08]
                elif direction == 'right':
                                 #left       #right    #up    #down
                    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]

                    weights = [0.04, 0.8, 0.08, 0.08]

                # Check if the neighboring entry exists and assign the value accordingly
                for neighbor, weight in zip(neighbors, weights):
                    if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                        neighbor_value = arr[neighbor]
                        result_dict[(i, j)] = (weight, neighbor) if neighbor_value == 1 else (1, (i, j))

    return result_dict

# Example usage:
arr = np.array([[0, 0, 1],
                [1, 1, 0],
                [1, 0, 1]])



def generate_state_action_pairs(state_matrix):

    directions = ['up', 'down', 'left', 'right']
    state_action_pairs=[]
    for direction in directions:
        state_action_pairs.append(create_directional_dictionary(arr, direction))
        #print(f"{direction}: {state_action_pairs}")
    return state_action_pairs
# Assuming you have a list of dictionaries, each representing a state-action pair


#print(generate_state_action_pairs(arr))

"""
        INPUT FORMAT
state_action_pairs = [
    {(x1, y1): (probability1, (x2, y2)), ...},
    {(x1, y1): (probability2, (x2, y2)), ...},
    # Add more dictionaries as needed
]

convert to 
 
        TRANSISIONS
        
        |S| x |A| x |S|
         s     a     s'
         T[s][a][s'] -> P(s'|a,s)

# Now T[s][a][s'] contains the probability of transitioning from state s to s' given action a
print(T[2][3][5])
 """
""" def getTransitions(state_action_pairs):
    list_of_dicts = state_action_pairs

    # Step 1: Determine unique states s and s'
    unique_states = set()
    for d in list_of_dicts:
        unique_states.add(next(iter(d)))
        unique_states.add(d[next(iter(d))][1])

    # Step 2: Create a mapping from states to indices
    state_to_index = {state: index for index, state in enumerate(unique_states)}

    # Step 3: Initialize the 3D numpy array
    num_states = len(unique_states)
    num_actions = len(list_of_dicts)
    T = np.zeros((num_states, num_actions, num_states))

    # Step 4: Populate the array with probabilities
    for action, d in enumerate(list_of_dicts):
        s = next(iter(d))
        s_prime = d[s][1]
        prob = d[s][0]
        
        s_index = state_to_index[s]
        s_prime_index = state_to_index[s_prime]
        
        T[s_index, action, s_prime_index] = prob

    # Now T is the 3D numpy matrix
    return T """

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
def getTransitions():

    floor_plan = "/home/saleeq/Desktop/new_map_planning_1.png"
    state_matrix, centers_dict,belief_ref = beliefgen.get_states(floor_plan)
    #print(belief_ref)
    #print(state_matrix)
    state_action_pairs = generate_state_action_pairs(state_matrix)
    #print(state_action_pairs)
    

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
    #print(belief_state_neighbours)
    #for each action, map the belief state to itself with probability of 1 if there is a blocked action in neighbours
    # up row1 
    # down row2
    # right row3
    # left row4

    for belief_state in belief_ref.keys():
        belief_neighbour_list = belief_state_neighbours[belief_state]
        #print(belief_neighbour_list)
        #check up 👆
        belief_idx = belief_state_indeces[belief_state]
        #probability that the robot will be dumb and won't do anything = 0.05 😄
        Tr[belief_state][0][belief_state]=0.05
        #if there is something on top 
        if (belief_idx[0]-1,belief_idx[1]) in belief_neighbour_list:
            #check if its not blocked
            if state_matrix[belief_idx[0]-1,belief_idx[1]]:
                #transition matrix of belief_state,up,state_up is 0.8

                Tr[belief_state][0][int(index_state_matrix[belief_idx[0]-1,belief_idx[1]]-1)]=0.95
            else:
                #place is blocked. map belif state to itself with probability 1
                Tr[belief_state][0][belief_state]=1
        #nothing on top also means blocked 🤦🏻‍♂️🤦🏻‍♂️
        else:
            Tr[belief_state][0][belief_state]=1
        
        #Robot has a higher probability of ending up in top neighbours if they exist
        #








        Tr[belief_state][1][belief_state]=0.05       
        #if there is something below       
        if (belief_idx[0]+1,belief_idx[1]) in belief_neighbour_list:
            #check if its not blocked
            if state_matrix[belief_idx[0]+1,belief_idx[1]]:
                #transition matrix of belief_state,down,state down is 0.8

                Tr[belief_state][1][int(index_state_matrix[belief_idx[0]+1,belief_idx[1]]-1)]=0.95
            else:
                #place is blocked. map belif state to itself with
                Tr[belief_state][1][belief_state]=1 
        else:
            Tr[belief_state][1][belief_state]=1 
        Tr[belief_state][2][belief_state]=0.05
        #if there is something on right
        if (belief_idx[0],belief_idx[1]+1) in belief_neighbour_list:
            #check if its not blocked
            if state_matrix[belief_idx[0],belief_idx[1]+1]:
                #transition matrix of belief_state,right,state right is 0.8

                Tr[belief_state][2][int(index_state_matrix[belief_idx[0],belief_idx[1]+1]-1)]=0.95
            else:
                #place is blocked. map belif state to itself with
                Tr[belief_state][2][belief_state]=1 
        else:
            Tr[belief_state][2][belief_state]=1 


            
        Tr[belief_state][3][belief_state]=0.05
        #if there is something on left
        if (belief_idx[0],belief_idx[1]-1) in belief_neighbour_list:
            #check if its not blocked
            if state_matrix[belief_idx[0],belief_idx[1]-1]:
                #transition matrix of belief_state,left,state left is 0.8

                Tr[belief_state][3][int(index_state_matrix[belief_idx[0],belief_idx[1]-1]-1)]=0.95
            else:
                #place is blocked. map belif state to itself with
                Tr[belief_state][3][belief_state]=1 
        else:
            Tr[belief_state][3][belief_state]=1 

    return Tr