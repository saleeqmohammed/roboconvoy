
import sys
import tools.datamanagement as datamanagement
import numpy as np
import pomdp.problem_maker as pmaker
import pomdp.pbVI as pbvi
import rospy

from std_msgs.msg import Int32,String
#availability_matrix =datamanagement.load_object("/home/saleeq/catkin_ws/src/roboconvoy/src/pomdp/availability_matrix.pickle")

###############################################################################################
#Define global variable for character_x,character_y
character_x = None
character_y =None
robot_i=None
robot_j =None
GRID_SIZE=None
#set goal
goal_state =50
starting_state=46
#puth the bot in the world
new_state = starting_state
#this is the size of the 🤖's world
observation =95
GRID_SIZE=50


#  DEFINE A FEW HELPER FUNCTIONS
#Define a funciton to normalize our belief 💡
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
def normalize_2drows_sum_to_1(array):
    row_sums = np.sum(array, axis=1, keepdims=True)
    normalized_array = array / row_sums
    return normalized_array

def create_numbered_state_matrix(state_matrix):
    count_matrix =np.ones_like(state_matrix)
    s_num =0
    for i in range(count_matrix.shape[0]):
        for j in range(count_matrix.shape[1]):
            count_matrix[i,j]=s_num
            s_num+=1
    return count_matrix
#Lets make the bot move
def move(matrix, index, direction, numbered_state_matrix):
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
            global robot_i,robot_j
            robot_i =i
            robot_j =j
            return True
        else:
            # Don't move if not possible
            return False
            #return robot_i, robot_j
    else:
        # Don't move if not possible
        return False
        #return robot_i, robot_j

# Example usage:
# robot_i, robot_j = move(matrix, index, 'up', numbered_state_matrix, robot_i, robot_j)

##########################################
# Initialize character


#Define stuff that 🤖 can do
#create our observer
def actual_observations_generator():
    # Implement logic to generate actual observations dynamically
    global robot_i,robot_j
    #100% accurate obs for now
    observed_state = numbered_state_matrix[robot_i,robot_j]
    return observed_state # Replace with your dynamic generation logic

""" def observe():
    global character_x,character_y
    obsesrved_i,observed_j =(character_y//GRID_SIZE)-1,(character_x//GRID_SIZE)-1
    observed_state = numbered_state_matrix[obsesrved_i,observed_j]
    return observed_state
 """

availability_matrix=np.array([   [0, 0, 0, 0, 0, 0, 0, 0, 0]
                                ,[0, 0, 1, 1, 1, 1, 1, 1, 0]
                                ,[0, 0, 1, 1, 1, 1, 1, 1, 0]
                                ,[0, 0, 1, 1, 1, 1, 1, 1, 0]
                                ,[0, 0, 0, 0, 1, 0, 1, 1, 0]
                                ,[0, 0, 0, 0, 1, 0, 0, 1, 0]
                                ,[0, 0, 0, 0, 1, 0, 0, 1, 0]
                                ,[0, 0, 0, 0, 1, 0, 1, 1, 0]
                                ,[0, 0, 0, 0, 1, 0, 1, 0, 0]
                                ,[0, 0, 0, 0, 1, 0, 1, 1, 0]
                                ,[0, 0, 0, 0, 1, 0, 1, 1, 0]
                                ,[0, 1, 1, 1, 1, 1, 1, 1, 0]
                                ,[0, 1, 1, 0, 1, 0, 0, 0, 0]
                                ,[0, 1, 1, 0, 1, 1, 1, 1, 0]
                                ,[0, 1, 1, 0, 1, 1, 1, 1, 0]
                                ,[0, 1, 1, 0, 1, 1, 1, 1, 0]
                                ,[0, 0, 0, 0, 0, 0, 0, 0, 0]])

availability_matrix=availability_matrix[1:-1,1:-1]

state_matrix =np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1]])
#we need to convert the grid to states
#lets make a numbered state matrix to do this 
numbered_state_matrix =create_numbered_state_matrix(state_matrix)




def make_decision(state_matrix,starting_state):
    
    #Lets solve the POMDP!!! 💪
    #Define S A T O R
    #set robot start conditions
    starting_idx = get_indeces(starting_state,state_matrix)

    global robot_i,robot_j
    robot_i=starting_idx[0]
    robot_j=starting_idx[1]
    #1. S -> states are defined in state_matrix 🙌 |S|

    #2. A -> actions ⏩ |A|
    actions={0:'up',1:'down',2:'right',3:'left'}

    #3. T -> Transition matrix 🔀 |S| x |A| x |S'|
    cT =pmaker.get_transition(state_matrix=state_matrix,actions=actions)

    #4. O -> Observation matrix omega |a| x |S| x |O|
    cOmega =pmaker.get_Omega(state_matrix=state_matrix,actions=actions)

    #4. R -> Rewards matrix R |S| x |A|
    cR =pmaker.get_rewards(state_matrix,actions,goal_state)
    #print(availability_matrix)
    #print(cT)
    #print(cOmega)
    #print(cR)



    #store the policy and loop through for viz
    policy=[]

    #Lets make our initial belief
    #defining a uniform belief vector

    #lets set all the blocked states to zero probability
    availability_vector=state_matrix.copy()
    availability_vector=availability_vector.flatten()
    #b1[availability_vector]=0
    #B=np.stack(b1,b2)
    #do an element wise multiplication

    B = np.ones((2,state_matrix.size))

    B = normalize_2drows_sum_to_1(B)

    #Lets generate a value distribution as well
    #initialize all 0 values
    V =np.zeros((1,state_matrix.size),np.float64)

    #🕓we need a Time horizon as well this defines how many steps ahead are we looking
    #an important part in pbvi

    T =4
    #Discount factor gamma
    gamma =1
    #Now lets define a pbvi object from our pbvi 
    apbvi =pbvi.PBVI(cT,cOmega,cR,gamma)


    pbvi_solver = pbvi.generator(apbvi,V,B,T)
    #iterating for set time should be till conveergence


    policy=[]
    movement_budget =30
    max_itr=0
    V,best_action_for_beliefs_vec=next(pbvi_solver)
    
    reward =0
    for mmt in range(movement_budget):
        
        #make an observation to get the belief 🔍
        #this is some wierd stuff get some real observation
        global observation
        current_belief = np.ones((1,105),dtype=np.float64)
        current_belief[0][observation] =10000
        current_belief = current_belief/np.sum(current_belief,axis=0,keepdims=True)
        # V is m X n belief is 1 x n 
        current_belief =current_belief.squeeze()
        cumulative_rewards =np.dot(V,current_belief)
        sorted_indices = np.argsort(cumulative_rewards)
        sorted_actions = best_action_for_beliefs_vec[sorted_indices]
        sorted_actions_explicit =[actions[action] for action in sorted_actions]
        high_value_action = sorted_actions[0]
        print(sorted_actions_explicit)
        #best action will have higest cumulative  reward
        best_action_index = np.argmax(cumulative_rewards)
        print(f'cumulative reward: {cumulative_rewards[best_action_index]}')
        best_action = best_action_for_beliefs_vec[best_action_index]

        #this one for highest value
        best_action=high_value_action

        #get all the actions, count immediate reward and take the one with highest immediate reward
    #    unique_actions, counts = np.unique(sorted_actions)
    #    immediate_reward_weight = [cR[observation,action]*count for count,action in zip(unique_actions,counts)]

        #sort this
        #best_action=high_value_action
        print(f'best action to take:{actions[best_action]}')
        #take best action
        
        moved =move(state_matrix,(robot_i,robot_j),actions[best_action],numbered_state_matrix)
        #if suggeste aciton is possible move the robot
        if moved:
            policy.append(actions[best_action])
            

        #once moved make an observation, update the belief space
        global new_state
        new_state = actual_observations_generator()
        #observation_old = observation
        response =[current_belief,best_action,observation]
        for __ in range(3):
            V,best_action_for_beliefs_vec =pbvi_solver.send(response)
        print(f'observed state:{ observation}')
        if observation == goal_state:
            print("👑 Goal!!!")
            break
    
        reward+=cR[observation,best_action]
        print(f'reward:{reward}')

    #fixed iteration method
    """ for __ in range(5):
        V,best_action_for_beliefs_vec =next(pbvi_solver) """


    print("all moved planned / buget expended!")
    print(f'policy: {policy}')



def integer_callback(msg, pub):
    state_matrix =np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1]])
    result = msg.data
    #sending observaton
    global observation
    observation = msg.data
    make_decision(state_matrix,95)
    
    rospy.loginfo(f'Received: {msg.data}, Result: {result}')
    #publish action
    global new_state
    pub.publish(new_state)
    #wait for action to complete before new decision


def result_node():
    rospy.init_node('result_node', anonymous=True)
    state_matrix =np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1]])
    starting_state =48
    #start make_decision generator
    global observation
    observation=starting_state
    
    pub = rospy.Publisher('/next_state', Int32, queue_size=10)
    rospy.Subscriber('/curr_state', Int32, integer_callback, pub)
    rospy.spin()

if __name__ == '__main__':
    state_matrix =np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1]])
    try:
        result_node()
    except rospy.ROSInterruptException:
        pass
