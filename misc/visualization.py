import pygame
import sys
import tools.datamanagement as datamanagement
import numpy as np
import problem_maker as pmaker
import pbVI as pbvi
#availability_matrix =datamanagement.load_object("/home/saleeq/catkin_ws/src/roboconvoy/src/pomdp/availability_matrix.pickle")

###############################################################################################
#Define global variable for character_x,character_y
character_x = None
character_y =None
robot_i=None
robot_j =None
GRID_SIZE=None
#set goal
goal_state =90
starting_state=40
#puth the bot in the world

#this is the size of the 🤖's world

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


#set robot start conditions
starting_idx = get_indeces(starting_state,state_matrix)

robot_i=starting_idx[0]
robot_j=starting_idx[1]
character_x, character_y = GRID_SIZE*(robot_j), (robot_i) * GRID_SIZE



#Lets solve the POMDP!!! 💪
#Define S A T O R

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
B[0][starting_state]=1000
B[1][starting_state]=1000
B = normalize_2drows_sum_to_1(B)

#Lets generate a value distribution as well
#initialize all 0 values
V =np.zeros((1,state_matrix.size),np.float64)

#🕓we need a Time horizon as well this defines how many steps ahead are we looking
#an important part in pbvi
T =10
#Discount factor gamma
gamma =1
#Now lets define a pbvi object from our pbvi 
apbvi =pbvi.PBVI(cT,cOmega,cR,gamma)


pbvi_solver = pbvi.generator(apbvi,V,B,T)
#iterating for set time should be till conveergence


#V convergence not the best!!
"""
while True:
    V_old =V.copy()
    V,best_action_for_beliefs_vec =next(pbvi_solver)
    Verr= np.linalg.norm(V - V_old, ord=np.inf)
    itr+=1
    print(f'iteration:{itr}')
    print(B.shape)
    print(best_action_for_beliefs_vec)
    if Verr < convergence_lim:

        break
"""

def find_best_belief_state(Epsi):
    # Sum the Epsi values over actions and observations for each belief state
    cumulative_rewards = np.sum(Epsi, axis=(0, 1))

    # Select the belief state index with the highest cumulative reward
    best_belief_state = np.argmax(cumulative_rewards)

    return best_belief_state




most_probable_belief_old =B[0].copy()
movement_budget =20
max_itr=20
V,best_action_for_beliefs_vec ,B=next(pbvi_solver)
reward =0
for mmt in range(movement_budget):
    itr=0
    # Is this a good idea? should iterate more?
    convergence_lim=1e-6
    while True:
        #iterate till best belief convergence
        #extimate best action

    # After the iterations, find the most probable belief state
        print(V.shape)
        print(best_action_for_beliefs_vec.shape)
        print(B.shape)
        #most probable belief
        most_probable_belief_index = np.argmax(np.sum(B, axis=1))
        most_probable_belief = B[most_probable_belief_index]
        bel_err = np.linalg.norm(most_probable_belief_old-most_probable_belief,ord=np.inf)

        #higest reward
        #most_rewarded =find_best_belief_state(Epsi)
        #REWARD 
        
        #print(f'best reward action: {actions[pbvi.best_action(most_rewarded,V,best_action_for_beliefs_vec)]}')
    


        most_probable_belief_old=most_probable_belief
        best_action = pbvi.best_action(most_probable_belief,V,best_action_for_beliefs_vec)
        itr+=1
        print(f'iteration:{itr}')
        observation = actual_observations_generator()
        response =[most_probable_belief,best_action,observation]
        V,best_action_for_beliefs_vec ,B=pbvi_solver.send(response)
        reward+=cR[observation,best_action]
        print(f'reward:{reward}')
        #print(f'observed state{observation}')
        if observation == goal_state:
            print("👑 Goal!!!")
            break
        if bel_err<convergence_lim:
            break
        
    #determine best action with most probable belief ? or most reward?
    best_action = pbvi.best_action(most_probable_belief,V,best_action_for_beliefs_vec)
    print(f'best action to take:{actions[best_action]}')

    moved =move(state_matrix,(robot_i,robot_j),actions[best_action],numbered_state_matrix)
    #if suggeste aciton is possible move the robot
    if moved:
        policy.append(actions[best_action])
    
    #once moved make an observation
    observation = actual_observations_generator()
    response =[most_probable_belief,best_action,observation]
    V,best_action_for_beliefs_vec ,B=pbvi_solver.send(response)
    print(f'observed state{ observation}')
    if observation == goal_state:
        print("👑 Goal!!!")
        break

    #update he belief state with observations

    



#fixed iteration method
""" for __ in range(5):
    V,best_action_for_beliefs_vec =next(pbvi_solver) """


print("all moved planned / buget expended!")
print(f'policy: {policy}')
#do a visualization
# Initialize Pygame
pygame.init()




WIDTH, HEIGHT = GRID_SIZE * availability_matrix.shape[0], GRID_SIZE * availability_matrix.shape[1]
CHARACTER_SIZE = GRID_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED=(255,0,0)
# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid World")

# Initialize grid
grid = [[WHITE for _ in range(WIDTH // GRID_SIZE)] for _ in range(HEIGHT // GRID_SIZE)]



character_speed = GRID_SIZE
#policy = ["up", "right","up","up","right","right","right","right","right","right","right","right","right", "up","up","right","right","right","right","up"]
current_action = 0

# Add targets and obstacles to the grid
goal_indeces = get_indeces(goal_state,state_matrix)

grid[goal_indeces[0]][goal_indeces[1]] = GREEN  # Example target cell


# Game loop
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and current_action<len(policy):
                # Perform action from the array
                if policy[current_action] == "up":
#                    global character_x,character_y
                    character_y -= character_speed
                elif policy[current_action] == "down":
#                    global character_x,character_y
                    character_y += character_speed
                elif policy[current_action] == "left":
 #                   global character_x,character_y
                    character_x -= character_speed
                elif policy[current_action] == "right":
#                    global character_x,character_y
                    character_x += character_speed

                current_action = (current_action + 1) % len(policy)
            else:
                print(f'policy used up had {len(policy)}, current move: {current_action}')







    # Draw grid with outlines
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pygame.draw.rect(screen, grid[row][col], (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
            
    #draw blocked_states
    for x in range(availability_matrix.shape[0]):
        for y in range(availability_matrix.shape[1]):
            if not availability_matrix[x, y]:
                #print(availability_matrix[x, y])
                #grid[y][x] = BLACK
                row=y
                col=x
                pygame.draw.rect(screen, grid[row][col], (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, RED, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 5)

    pygame.draw.rect(screen, BLUE, (character_x, character_y, CHARACTER_SIZE, CHARACTER_SIZE))
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            font = pygame.font.Font(None, 36)  # You can adjust the font size as needed
            text = font.render(f"{row * len(grid[row]) + col}", True, BLACK)
            text_rect = text.get_rect(center=(col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))
            screen.blit(text, text_rect)

# Draw character
#    global character_x,character_y

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
