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
s_term =4
#define the availability_matrix / availability matrix
availability_matrix =np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
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
            return [0,(1000,1000)]
    else:
        return [0,(1000,1000)]

def get_number_from_indices(matrix, indices):
    count_matrix =np.ones_like(matrix)
    if indices[0]==1000:
        global s_term
        return s_term
    s_num =0
    for n in range(matrix.size):
        if find_nth_one(n,matrix) == indices:
            return n
            print(f'Num {n}')

#🚨 i am messing this function up

def find_nth_one( n,matrix):
    """
    Finds the position of the nth '1' in a 2D numpy array, moving from top left to bottom right.

    :param matrix: 2D numpy array
    :param n: Order of the '1' to find (0-based index)
    :return: Tuple (row, column) of the nth '1', or None if not found
    """
    count = 0
    rows, cols = matrix.shape
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1:
                if count == n:
                    return (i, j)
                count += 1
    return (1000,1000)


            
def move_robot(action,availability_matrix,curr_state):
    curr_state_idx =find_nth_one(curr_state,availability_matrix)
    
    return check_direction(availability_matrix,curr_state_idx,action),
        
print(move_robot('down',availability_matrix,1))
#reward generator 👑
#this is the old one I was being dumb 
""" def get_reward(goal_state,availability_matrix,actions):
    num_actions
    cR = np.ones(grid_size)*-1
    goal_state =find_nth_one(goal_state,availability_matrix)
    cR[goal_state[0],goal_state[1]]=40
    return cR """
def eculidian(availability_matrix,state,goal_state):
    state_idx = find_nth_one(state,availability_matrix)
    goal_idx = find_nth_one(goal_state,availability_matrix)
    return np.sqrt((state_idx[0]-goal_idx[0])**2 +(state_idx[1]-goal_idx[1])**2 )
def get_rewards(availability_matrix,actions,goal_state):
    #Rewars is |A| x |s|
    #given state, what is the reward for taking action a?
    num_states = np.count_nonzero(availability_matrix)+1 #s_i U s_term
    s_term=num_states-1
    num_acitons =len(actions)
    #initialize with -1 reward so that 🤖 does not make unnecessary moves.
    R=np.ones((num_states,num_acitons),dtype=np.float64)*-10
    #for each state if action is possible, 
    # give a reward of -1 
    # else -10 to deter from running into blocks
    for state in range(num_states):
        for action in range(num_acitons):
            #try moving
            movement = move_robot(actions[action],availability_matrix,state)
            #if movement possible non zero probability is returned
            if movement[0][0]!=0:
                #check if we are reaching goal state
                new_state_idx =movement[0][1]
                if get_number_from_indices(availability_matrix,new_state_idx)==goal_state:
                    #assign reward 50 to encourage the 🤖 :robot_face
                    R[state,action]=2350
                else:
                    #set reward to -1
                    R[state,action]=-1#-eculidian(availability_matrix,state,goal_state)/3
            #⛔for blocked / restricted / non-existing states
            else:
                R[state,action]=-500
    eculidian_matrix =np.zeros_like(availability_matrix,dtype=np.float64)
    for i in range(availability_matrix.shape[0]):
        for j in range(availability_matrix.shape[1]):
            eculidian_matrix[i,j]=eculidian(availability_matrix,get_number_from_indices(availability_matrix,(i,j)),goal_state)/1
    print(eculidian_matrix)
    return R

cR =get_rewards(availability_matrix,actions,2)
print("Rewards!!!")
print(cR)

""" def get_transition(availability_matrix,actions):
    
    num_states = np.count_nonzero(availability_matrix)+1 #s_i U s_term
    s_term=num_states-1
    num_actions =len(actions)
    num_final_states=num_states
    cT =np.zeros((num_states,num_actions,num_states),dtype=np.float64)
    for starting_state in range(num_states):
        action_final_availability_matrix =np.zeros((num_actions,num_final_states))
        #iterate through each action 1up 2down 3right 4left
        action_idx =0
        for action_matrix in action_final_availability_matrix:
            
            #this is the probability that the transition happens
            movement=move_robot(actions[action_idx],availability_matrix,starting_state)
            probability=movement[0][0]
            final_state_idx=movement[0][1]
            
            final_state =get_number_from_indices(availability_matrix,final_state_idx)
                
            #if this transition happens, add 0.9 to final state that the robot would reach
            # and 0.1 to the current state to account for failure
            if probability!=0:
                cT[starting_state,action_idx,final_state]=probability
                cT[final_state,action_idx,starting_state]=1-probability
            else:
                
                cT[s_term,action_idx,starting_state]=1
            action_idx+=1
    return cT """
def get_transition(availability_matrix,actions):
        #given state, what is the reward for taking action a?
    num_states = np.count_nonzero(availability_matrix)+1 #s_i U s_term
    s_term=num_states-1
    num_actions =len(actions)
    num_final_states=num_states
    # T |S| X |A| X |S'|
    cT =np.zeros((num_states,num_actions,num_states),dtype=np.float64)
    for starting_state in range(num_states):
        action_final_state_matrix =np.zeros((num_actions,num_final_states))
        #iterate through each action 0up 1down 2right 3left
        action_idx =0
        for action_matrix in action_final_state_matrix:
            
            #this is the probability that the transition happens
            movement=move_robot(actions[action_idx],availability_matrix,starting_state)
            probability=movement[0][0]
            final_state_idx=movement[0][1]
            


            final_state =get_number_from_indices(availability_matrix,final_state_idx)
                
            #if this transition happens, add 0.9 to final state that the robot would reach
            # and 0.1 to the current state to account for failure
            if probability!=0:
                cT[starting_state,action_idx,starting_state]=1.0-probability
                cT[starting_state,action_idx,final_state]=probability
                
                
            else:
                cT[starting_state,action_idx,s_term]=1
            action_idx+=1
    return cT

cT = get_transition(availability_matrix,actions)
def get_transition_update(availability_matrix,actions):
    num_states = np.count_nonzero(availability_matrix)+1 #s_i U s_term
    s_term=num_states-1
    num_actions =len(actions)
    num_final_states=num_states
    cT =np.zeros((num_states,num_actions,num_states),dtype=np.float64)
    for final_state in range(num_states):
        starting_action_availability =np.zeros((num_actions,num_states))
        pass

cT = get_transition(availability_matrix,actions)
print("Transition")
print(cT)

def get_Omega(availability_matrix,actions):
    num_actions = len(actions)
    num_states = np.count_nonzero(availability_matrix)+1 #s_i U s_term
    s_term=num_states-1
    num_observations = num_states
    #if i can move down to a valid state , i have 80% probable final_state for up
    cOmega = np.ones((num_actions,num_states,num_observations),dtype=np.float64)
    for action in range(num_actions):
        for state in range(num_states):
            #if action is up check if we can move down
            if actions[action]=='up':

                movement =move_robot('down',availability_matrix,state)
                #if we can move probability is not zero
                if 0!=movement[0][0]:
                    #since we are checking opposite we can map to same state
                    cOmega[action][state][state] = 4*num_observations
                #if not probability of terminal obervation / null observation is 1
                else:
                    cOmega[action][state][s_term]=8*num_observations
             #if action is dowm check if we can move up
            if actions[action]=='down':

                movement =move_robot('up',availability_matrix,state)
                #if we can move probability is not zero
                if 0!=movement[0][0]:
                    #since we are checking opposite we can map to same state
                    cOmega[action][state][state] = 4*num_observations
                #if not probability of terminal obervation / null observation is 1
                else:
                    cOmega[action][state][s_term]=8*num_observations
                
             #if action is right check if we can move left
            if actions[action]=='right':

                movement =move_robot('left',availability_matrix,state)
                #if we can move probability is not zero
                if 0!=movement[0][0]:
                    #since we are checking opposite we can map to same state
                    cOmega[action][state][state] = 4*num_observations
                #if not probability of terminal obervation / null observation is 1
                else:
                    cOmega[action][state][s_term]=8*num_observations
             #if action is left check if we can move up
            if actions[action]=='left':

                movement =move_robot('right',availability_matrix,state)
                #if we can move probability is not zero
                if 0!=movement[0][0]:
                    #since we are checking opposite we can map to same state
                    cOmega[action][state][state] = 4*num_observations
                #if not probability of terminal obervation / null observation is 1
                else:
                    cOmega[action][state][s_term]=8*num_observations
    #now that we have omega we have to normalize it
    cOmega = normalize_rows_sum_to_1(cOmega)
    return cOmega
cOmega = get_Omega(availability_matrix,actions)
""" print(cOmega)
print(cOmega.shape)
 """







