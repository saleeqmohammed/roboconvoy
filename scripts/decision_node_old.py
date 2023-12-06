import datamanagement
import pomdp.pbvi
import pomdp.belief_state_gen as beliefgen
import numpy as np
import pomdp.transition_s_a_sp as transition
#states = datamanagement.load_object("src/pomdp/beliefstates.pickle")
#beliefstate_reference = datamanagement.load_object("src/pomdp/beliefstate_reference.pickle")
"""
        STATES
        states are defined as coordinates of center of grid cells
        for n states if we have m belief states,
        B
          m x n
"""
floor_plan = "/home/saleeq/Desktop/new_map_planning_1.png"
state_matrix, centers_dict,img_ref = beliefgen.get_states(floor_plan)
#initial belief state of equal probabilities
b_init = np.array(list(centers_dict.values()))
b_init = [p_s/np.sum(b_init) for p_s in b_init]
B=[b_init]
print(len(B[0]))
#print(B)

# add more belief states if needed

#we have states, but given target state/ goal state to keep the object in , what is the new belief states/available states?
#not necessasry: bots need to make it to the target.
"""
        ACTIONS
"""
actions =['up','down','right','left']

"""
        TRANSISIONS
        
        |S| x |A| x |S|
         s     a     s'
         T[s][a][s'] -> P(s'|a,s)

Lay a few ground rules to define this
if we try to move to impossible state (moving up at topmost) -> 0
successful transition has 88% probability ? (need to model)
rest 15% divided with 5% right 5% left 2% bottom in case of up. set similar rules.
"""
#0 up 1 down 2 right 3 left
T =transition.getTransitions()
print(T[3][3][2])

"""
        R(s,a)
        |S| x |A|

"""

#rewards R(s,a) return the cost of taking actino a at given current state s
#as per model we need to return 
def get_rewards(beliefstates,beliefstate_reference,n_start ,n_target):
    #coordinates are states 
    goal_coordinates = beliefstate_reference[n_target]
    current_belif_coordinates = cur