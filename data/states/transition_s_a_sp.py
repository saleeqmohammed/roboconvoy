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
                    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                    weights = [0.8, 0.04, 0.08, 0.08]
                elif direction == 'down':
                    neighbors = [(i+1, j)]
                    weights = [0.8]
                elif direction == 'left':
                    neighbors = [(i, j-1)]
                    weights = [0.8]
                elif direction == 'right':
                    neighbors = [(i, j+1)]
                    weights = [0.8]

                # Check if the neighboring entry exists and assign the value accordingly
                for neighbor, weight in zip(neighbors, weights):
                    if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                        neighbor_value = arr[neighbor]
                        result_dict[(i, j)] = (weight, neighbor) if neighbor_value == 1 else (1, (i, j))

    return result_dict

# Example usage:
arr = np.array([[1, 0, 1],
                [0, 1, 0],
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
def getTransitions(state_action_pairs):
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
    return T


floor_plan = "/home/saleeq/Desktop/new_map_planning_1.png"
state_matrix, centers_dict,img_ref = beliefgen.get_states(floor_plan)
print(state_matrix)
state_matrix = state_matrix.T 
state_matrix = state_matrix[1:-1,1:-1]
print(state_matrix)
print(state_matrix.size)
state_action_pairs = generate_state_action_pairs(state_matrix)
print(state_action_pairs)
T =getTransitions(state_action_pairs)

print(T)