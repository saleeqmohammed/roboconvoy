#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

def integer_callback(msg):
    rospy.loginfo(f'Received: {msg.data}')

def integer_subscriber():
    rospy.init_node('integer_subscriber_node', anonymous=True)
    rospy.Subscriber('/expected_state', Int32, integer_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        integer_subscriber()
    except rospy.ROSInterruptException:
        pass
