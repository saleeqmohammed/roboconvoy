import datamanagement
states = datamanagement.load_object("src/pomdp/beliefstates.pickle")
beliefstate_reference = datamanagement.load_object("src/pomdp/beliefstate_reference.pickle")

#we have states, but given target state/ goal state to keep the object in , what is the new belief states/available states?
#not necessasry: bots need to make it to the target.

#Transitions
"""

        |S| x |A| x |S|
         s     a     s'
         T[s][a][s'] -> P(s'|a,s)

Lay a few ground rules to define this
if we try to move to impossible state (moving up at topmost) -> 0
successful transition has 88% probability ? (need to model)
rest 15% divided with 5% right 5% left 2% bottom in case of up. set similar rules.
"""



#rewards R(s,a) return the cost of taking actino a at given current state s
#as per model we need to return 
def get_rewards(beliefstates,beliefstate_reference,n_start ,n_target):
    #coordinates are states 
    goal_coordinates = beliefstate_reference[n_target]
    current_belif_coordinates = cur