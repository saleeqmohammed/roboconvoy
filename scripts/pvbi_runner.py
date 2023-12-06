#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

class PublishExpectedStateNode:
    def __init__(self):
        rospy.init_node('publish_expected_state_node', anonymous=True)
        self.expected_state_publisher = rospy.Publisher('/expected_state', Int32, queue_size=10)
        self.rate = rospy.Rate(1)  # Publish at a rate of 1 Hz

    def run(self):
        states =[95,96,81,82,83,84,85,70,55,56,57,72,73]
        while not rospy.is_shutdown():
            
            for state in states:
                self.expected_state_publisher.publish(state)
            
                rospy.sleep(10)

if __name__ == '__main__':
    try:
        node = PublishExpectedStateNode()
        node.run()
    except rospy.ROSInterruptException:
        pass
