#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion

class MoveRobot:
    def __init__(self):
        rospy.init_node('move_robot_node', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_subscriber = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.rate = rospy.Rate(10)  # 10 Hz

    def odom_callback(self, odom_msg):
        orientation = odom_msg.pose.pose.orientation
        orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
        _, _, yaw = euler_from_quaternion(orientation_list)
        self.current_yaw = yaw

    def move_distance(self, distance):
        initial_x = 0.0
        current_x = 0.0
        linear_speed = 0.2  # Adjust as needed
        duration = distance / linear_speed

        twist_msg = Twist()
        twist_msg.linear.x = linear_speed

        start_time = rospy.get_time()

        while current_x - initial_x < distance and not rospy.is_shutdown():
            self.velocity_publisher.publish(twist_msg)
            current_time = rospy.get_time()
            current_x += linear_speed * (current_time - start_time)
            self.rate.sleep()

        twist_msg.linear.x = 0.0
        self.velocity_publisher.publish(twist_msg)

    def run(self):
        try:
            distance_to_move = 1.0  # Adjust as needed
            self.move_distance(distance_to_move)
        except rospy.ROSInterruptException:
            pass

if __name__ == '__main__':
    try:
        robot = MoveRobot()
        robot.run()
    except rospy.ROSInterruptException:
        pass
