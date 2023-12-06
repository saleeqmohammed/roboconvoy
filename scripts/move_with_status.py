#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sqrt
from std_msgs.msg import Bool  # Import Bool message type

class MoveRobot:
    def __init__(self):
        rospy.init_node('move_robot_node', anonymous=False)
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_subscriber = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.goal_subscriber = rospy.Subscriber('/goal', PoseStamped, self.goal_callback)
        self.move_completed_publisher = rospy.Publisher('/move_completed', Bool, queue_size=10)  # New publisher
        self.rate = rospy.Rate(10)  # 10 Hz
        self.current_pose = None
        self.goal_pose = None

    def odom_callback(self, odom_msg):
        self.current_pose = odom_msg.pose.pose

    def goal_callback(self, goal_msg):
        rospy.loginfo(goal_msg.pose)
        self.goal_pose = goal_msg.pose

    def get_distance_to_goal(self):
        if self.current_pose is not None and self.goal_pose is not None:
            dx = self.goal_pose.position.x - self.current_pose.position.x
            dy = self.goal_pose.position.y - self.current_pose.position.y
            return sqrt(dx**2 + dy**2)
        return float('inf')

    def get_angle_to_goal(self):
        if self.current_pose is not None and self.goal_pose is not None:
            _, _, current_yaw = euler_from_quaternion([self.current_pose.orientation.x, self.current_pose.orientation.y,
                                                       self.current_pose.orientation.z, self.current_pose.orientation.w])
            goal_yaw = atan2(self.goal_pose.position.y - self.current_pose.position.y,
                             self.goal_pose.position.x - self.current_pose.position.x)
            return goal_yaw - current_yaw
        return float('inf')

    def align_to_goal(self):
        angular_speed_crr = 0.7  # Adjust as needed

        while abs(self.get_angle_to_goal()) > 0.1 and not rospy.is_shutdown():
            angle_to_goal = self.get_angle_to_goal()

            twist_msg = Twist()
            twist_msg.angular.z = angular_speed_crr * angle_to_goal

            self.velocity_publisher.publish(twist_msg)
            self.rate.sleep()

        stop_msg = Twist()
        self.velocity_publisher.publish(stop_msg)

    def move_to_goal(self):
        linear_speed = 0.2  # Adjust as needed
        angular_speed = 0.5  # Adjust as needed

        while not rospy.is_shutdown():
            while self.goal_pose is None and not rospy.is_shutdown():
                self.rate.sleep()

            rospy.loginfo("Moving to goal...")
            #self.align_to_goal()
            while self.get_distance_to_goal() > 0.1 and not rospy.is_shutdown():
                angle_to_goal = self.get_angle_to_goal()
                self.align_to_goal()
                twist_msg = Twist()
                twist_msg.linear.x = linear_speed
                twist_msg.angular.z = angular_speed * angle_to_goal

                self.velocity_publisher.publish(twist_msg)
                self.rate.sleep()

            stop_msg = Twist()
            self.velocity_publisher.publish(stop_msg)

            # Publish whether the move to goal has been completed or not
            move_completed_msg = Bool()
            move_completed_msg.data = True
            self.move_completed_publisher.publish(move_completed_msg)

    def run(self):
        try:
            self.move_to_goal()
        except rospy.ROSInterruptException:
            pass

if __name__ == '__main__':
    try:
        robot = MoveRobot()
        robot.run()
    except rospy.ROSInterruptException:
        pass
