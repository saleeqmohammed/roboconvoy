#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry

def callback(msg):
    # Callback function to print the pose information
    rospy.loginfo("Odometry Pose:\n%s", msg.pose.pose)

def listener():
    # Initialize the ROS node
    rospy.init_node('odometry_listener', anonymous=True)

    # Subscribe to the odometry topic
    rospy.Subscriber('/odom', Odometry, callback)

    # Spin to keep the script alive
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
