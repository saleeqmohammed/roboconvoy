
#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
import time

def get_next_state(crst):
    available_states=[81,82,83,84,85,70,5,40,25]
    for i in range(len(available_states)):
        if available_states[i] == crst:
            return available_states[i+1]
def integer_callback(msg,pub):
    rospy.loginfo(f'Received: {msg.data}')
    crst = msg.data
    next_state = get_next_state(crst)
    pub.publish(next_state)
    time.sleep(30)

def integer_subscriber():
    rospy.init_node('integer_subscriber_node', anonymous=True)
    
    pub =rospy.Publisher('expected_state',Int32,queue_size=10)
    rospy.Subscriber('curr_state', Int32, integer_callback,pub)
    rospy.spin()

if __name__ == '__main__':
    try:
        integer_subscriber()
    except rospy.ROSInterruptException:
        pass
