#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
import numpy as np
from std_msgs.msg import String, Int32,Bool
def get_indeces(state_number, numbered_state_matrix):
    s_num = 0  # Initialize s_num
    for i in range(numbered_state_matrix.shape[0]):
        for j in range(numbered_state_matrix.shape[1]):
            numbered_state_matrix[i, j] = s_num
            if state_number == s_num:
                return (i, j)
            else:
                s_num += 1

def new_state(numbered_state_matrix,move,current_state):
    current_state_idx = get_indeces(current_state,numbered_state_matrix)
    if move =='up':
        i = current_state_idx[0]-1
        j = current_state_idx[1]
    if move =='down':
        i = current_state_idx[0]+1
        j = current_state_idx[1]
    
    if move =='left':
        i = current_state_idx[0]
        j = current_state_idx[1]-1
    
    if move =='right':
        i = current_state_idx[0]
        j = current_state_idx[1]+1
    return numbered_state_matrix[i,j]

def move_to_state(observation):
    stored_moves =['left','left','up','up','left']
    i=0
    while True and stored_moves:
        yield stored_moves[i]
        i-=1

state_matrix =np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1]])
numbered_state_matrix = np.array([[  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,
         13,  14],
       [ 15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,
         28,  29],
       [ 30,  31,  32,  33,  34,  35,  36,  37,  38,  39,  40,  41,  42,
         43,  44],
       [ 45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,  56,  57,
         58,  59],
       [ 60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,  71,  72,
         73,  74],
       [ 75,  76,  77,  78,  79,  80,  81,  82,  83,  84,  85,  86,  87,
         88,  89],
       [ 90,  91,  92,  93,  94,  95,  96,  97,  98,  99, 100, 101, 102,
        103, 104]])
class MovementManager:
    def __init__(self):
        
        rospy.loginfo("movement manger initilized")
        self.move_generator =move_to_state(1)
        
        self.current_state_subscriber = rospy.Subscriber('/curr_state', Int32, self.odom_state_callback)
        self.status_subscriber =rospy.Subscriber('/moved_status', Bool, self.status_callback)

        self.next_state_publisher =rospy.Publisher('/expected_state', Int32, queue_size=10)
        self.curr_state= None
        self.next_expected_state = self.curr_state
        self.moved_status =None
    def odom_state_callback(self,msg):

        self.curr_state =msg.data



    def status_callback(self,msg):

        self.moved_status =msg.data
            
    def move(self):
        while not rospy.is_shutdown():
            if self.moved_status:
                proposed_move = self.move_generator.send(self.curr_state)
                rospy.loginfo(f'current stat{ self.curr_state}')
                self.next_expected_state = new_state(numbered_state_matrix,proposed_move,self.curr_state)
            #get next move with pomdp
                self.next_expected_state =new_state(numbered_state_matrix,proposed_move,self.curr_state)
            self.next_state_publisher.publish(self.next_expected_state)
    def run(self):
        try:
            self.move()
        except rospy.ROSInterruptException:
            pass

if __name__ == '__main__':
    try:
        rospy.init_node('move_management_node', anonymous=False)
        movement_manger =MovementManager()
        movement_manger.run()
    except rospy.ROSInterruptException:
        pass
