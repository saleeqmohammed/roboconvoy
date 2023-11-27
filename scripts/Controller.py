#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist, PoseStamped
from std_msgs.msg import Header
import math

# Global variables to store the target pose and the current estimated pose
target_pose = PoseStamped()
estimated_pose = PoseStamped()

# Callback function to update the target pose
def target_pose_callback(msg):
    global target_pose
    target_pose = msg

# Callback function to update the current estimated pose
def estimated_pose_callback(msg):
    global estimated_pose
    estimated_pose = msg

def move_robot(robot_name, linear_speed, proportional_gain=1.0):
    rospy.init_node(f'robot1_controller', anonymous=True)
    pub = rospy.Publisher(f'robot_1/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    # Subscribe to the estimated pose and the current pose
    rospy.Subscriber(f'robot_1/estimated_pose', PoseStamped, estimated_pose_callback)
    rospy.Subscriber(f'robot_1/target_pose', PoseStamped, target_pose_callback)

    cmd_vel = Twist()

    while not rospy.is_shutdown():
        # Calculate the difference between estimated pose and target pose
        dx = target_pose.pose.position.x - estimated_pose.pose.position.x
        dy = target_pose.pose.position.y - estimated_pose.pose.position.y

        # Calculate the distance to the target position
        distance = math.sqrt(dx**2 + dy**2)

        # Avoid division by zero
        if distance != 0:
            # Adjust linear velocity based on the proportional control
            cmd_vel.linear.x = proportional_gain * linear_speed * dx / distance
            cmd_vel.linear.y = proportional_gain * linear_speed * dy / distance
        else:
            cmd_vel.linear.x = 0
            cmd_vel.linear.y = 0

        pub.publish(cmd_vel)
        rate.sleep()

if __name__ == '__main__':
    try:
        # Move robot1 to the target pose
        move_robot('robot1', 0.2)

       

    except rospy.ROSInterruptException:
        pass
