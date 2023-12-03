
import datamanagement
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import pbVI as pbvi
import problem_maker
#Grid size
grid_size =(3,3)
def normalize_2drows_sum_to_1(array):
    row_sums = np.sum(array, axis=1, keepdims=True)
    normalized_array = array / row_sums
    return normalized_array
#define the state_matrix / availability matrix
state_matrix=np.array([[1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1]])
#define the acitons
actions={0:'up',1:'down',2:'right',3:'left'}


cT = problem_maker.get_transition(state_matrix,actions)

cR = problem_maker.get_rewards(state_matrix,actions,goal_state=2)
cOmega = problem_maker.get_Omega(state_matrix,actions)
gamma = 1.0
apbvi = pbvi.PBVI(cT, cOmega, cR, gamma)

V = np.zeros((1, 9), np.float64)


B = np.ones((2,9))
B = normalize_2drows_sum_to_1(B)

if __name__ == '__main__':
                    #pvbi object #Values #Beliefs #Time horizon
    pbvi_gen = pbvi.generator(apbvi, V, B, 4)

    #iterate till convergence instea?
    for __ in range(5):
        V, best_to_do = next(pbvi_gen)
    print(V.shape)
    print(B.shape)
    print(best_to_do.shape)
    #instead of just expanding expand after belief update
    #B = 
    for _ in range(5):
        B = apbvi.expanded_B(B)
        #print(B)

    
  #V = np.zeros((1, 9), np.float64)


        #print(V)
        do_this =pbvi.best_action(B[0],V,best_to_do)
        print(actions[do_this])
        #print(V.shape)
        


 