#author Mohammed Saleeq K
# Uh oh this ones a problem maker 🤪
#!/usr/bin/ python3
import numpy as np
def normalize_rows_sum_to_1(array):
    row_sums = np.sum(array, axis=2, keepdims=True)
    normalized_array = array / row_sums
    return normalized_array
#Grid size
grid_size =(3,3)

#define the state_matrix / availability matrix
state_matrix =np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1]])

#define the actions
actions={0:'up',1:'down',2:'right',3:'left'}

def check_direction(matrix, index, direction):
    rows, cols = matrix.shape
    i, j = index

    if direction == 'up':
        i -= 1
    elif direction == 'down':
        i += 1
    elif direction == 'left':
        j -= 1
    elif direction == 'right':
        j += 1
    else:
        raise ValueError("Invalid direction. Use 'up', 'down', 'left', or 'right'.")

    # Check if the new indices are within the matrix bounds
    if 0 <= i < rows and 0 <= j < cols:
        if matrix[i, j] == 1:
            return [0.9,(i,j)]
        else:
            return [0,index]
    else:
        return [0,index]

def get_number_from_indices(matrix, indices):
    count_matrix =np.ones_like(matrix)
    s_num =0
    for i in range(count_matrix.shape[0]):
        for j in range(count_matrix.shape[1]):
            count_matrix[i,j]=s_num
            s_num+=1
    return count_matrix[indices[0],indices[1]]

#🚨 i am messing this function up
""" def get_indeces(state_number,state_matrix):
    state_coordinates={}
    #don't mess up teh state matrix
    state_matrix_tmp = np.copy(state_matrix)
    for i in range(state_matrix_tmp.shape[0]):
        for j in range(state_matrix_tmp.shape[1]):
            state_coordinates[i+j*grid_size[1]]=(j,i)
    return state_coordinates[state_number] """
def get_indeces(state_number,state_matrix):
    numbered_state_matrix = np.zeros_like(state_matrix)
    s_num =0
    for i in range(numbered_state_matrix.shape[0]):
        for j in range(numbered_state_matrix.shape[1]):
            numbered_state_matrix[i,j]=s_num
            if state_number==s_num:
                return (i,j)
            else:
                s_num+=1
def move_robot(action,state_matrix,curr_state):
    curr_state_idx =get_indeces(curr_state,state_matrix)
    
    return check_direction(state_matrix,curr_state_idx,action),
        
print(move_robot('down',state_matrix,1))
#reward generator 👑
#this is the old one I was being dumb 
""" def get_reward(goal_state,state_matrix,actions):
    num_actions
    cR = np.ones(grid_size)*-1
    goal_state =get_indeces(goal_state,state_matrix)
    cR[goal_state[0],goal_state[1]]=40
    return cR """
def get_rewards(state_matrix,actions,goal_state):
    #Rewars is |A| x |s|
    #given state, what is the reward for taking action a?
    num_states = state_matrix.size
    num_acitons =len(actions)
    #initialize with -1 reward so that 🤖 does not make unnecessary moves.
    R=np.ones((num_states,num_acitons))*-1
    #for each state if action is possible, 
    # give a reward of -1 
    # else -10 to deter from running into blocks
    for state in range(num_states):
        for action in range(num_acitons):
            #try moving
            movement = move_robot(actions[action],state_matrix,state)
            #if movement possible non zero probability is returned
            if movement[0][0]!=0:
                #check if we are reaching goal state
                new_state_idx =movement[0][1]
                if get_number_from_indices(state_matrix,new_state_idx)==goal_state:
                    #assign reward 50 to encourage the 🤖 :robot_face
                    R[state][action]=50
                else:
                    #set reward to -1
                    R[state][action]=-1
            #⛔for blocked / restricted / non-existing states
            else:
                R[state][action]=-50
    return R

cR =get_rewards(state_matrix,actions,2)
#print(cR)

def get_transition(state_matrix,actions):
    num_states = state_matrix.size
    num_actions =len(actions)
    num_final_states=num_actions
    cT =np.zeros((num_states,num_actions,num_states))
    for starting_state in range(num_states):
        action_final_state_matrix =np.zeros((num_actions,num_final_states))
        #iterate through each action 1up 2down 3right 4left
        action_idx =0
        for action_matrix in action_final_state_matrix:
            
            #this is the probability that the transition happens
            movement=move_robot(actions[action_idx],state_matrix,starting_state)
            probability=movement[0][0]
            final_state_idx=movement[0][1]
            
            final_state =get_number_from_indices(state_matrix,final_state_idx)
                
            #if this transition happens, add 0.9 to final state that the robot would reach
            # and 0.1 to the current state to account for failure
            if probability!=0:
                cT[starting_state][action_idx][final_state]=probability
                cT[starting_state][action_idx][starting_state]=1-probability
            else:
                cT[starting_state,action_idx,starting_state]=1
            action_idx+=1
    return cT

cT = get_transition(state_matrix,actions)

#print(cT)

def get_Omega(state_matrix,actions):
    num_actions = len(actions)
    num_states =state_matrix.size
    num_observations = num_states
    #if i can move down to a valid state , i have 80% probable final_state for up
    cOmega = np.ones((num_actions,num_states,num_observations))
    for action in range(num_actions):
        for state in range(num_states):
            #if action is up check if we can move down
            if actions[action]=='up':

                movement =move_robot('down',state_matrix,state)
                #if we can move probability is not zero
                if 0!=movement[0][0]:
                    #since we are checking opposite we can map to same state
                    cOmega[action][state][state] = 4*num_observations
             #if action is dowm check if we can move up
            if actions[action]=='down':

                movement =move_robot('up',state_matrix,state)
                #if we can move probability is not zero
                if 0!=movement[0][0]:
                    #since we are checking opposite we can map to same state
                    cOmega[action][state][state] = 4*num_observations
             #if action is right check if we can move left
            if actions[action]=='right':

                movement =move_robot('left',state_matrix,state)
                #if we can move probability is not zero
                if 0!=movement[0][0]:
                    #since we are checking opposite we can map to same state
                    cOmega[action][state][state] = 4*num_observations
             #if action is left check if we can move up
            if actions[action]=='left':

                movement =move_robot('right',state_matrix,state)
                #if we can move probability is not zero
                if 0!=movement[0][0]:
                    #since we are checking opposite we can map to same state
                    cOmega[action][state][state] = 4*num_observations
    #now that we have omega we have to normalize it
    cOmega = normalize_rows_sum_to_1(cOmega)
    return cOmega
cOmega = get_Omega(state_matrix,actions)
#print(cOmega)
#print(cOmega.shape)










