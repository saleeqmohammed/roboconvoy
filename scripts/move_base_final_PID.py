#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sqrt

class MoveRobot:
    def __init__(self):
        rospy.init_node('move_robot_node', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_subscriber = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.goal_subscriber = rospy.Subscriber('/move_base_simple/goal', PoseStamped, self.goal_callback)
        self.rate = rospy.Rate(10)  # 10 Hz
        self.current_pose = None
        self.goal_pose = None

        # PID Controller Parameters
        self.Kp = 1.0  # Proportional gain
        self.Ki = 0.0  # Integral gain
        self.Kd = 0.1  # Derivative gain
        self.prev_error = 0.0
        self.integral = 0.0

    def odom_callback(self, odom_msg):
        self.current_pose = odom_msg.pose.pose

    def goal_callback(self, goal_msg):
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

    def pid_controller(self, error):
        # PID Controller
        self.integral += error * self.rate.sleep_dur.to_sec()
        derivative = (error - self.prev_error) / self.rate.sleep_dur.to_sec()

        # Calculate control input
        control_input = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        self.prev_error = error

        return control_input

    def align_to_goal(self):
        angular_speed_crr = 0.7  # Adjust as needed

        while abs(self.get_angle_to_goal()) > 0.1 and not rospy.is_shutdown():
            angle_to_goal = self.get_angle_to_goal()

            # Use PID controller for angular velocity
            angular_speed = self.pid_controller(angle_to_goal)

            twist_msg = Twist()
            twist_msg.angular.z = angular_speed * angular_speed_crr

            self.velocity_publisher.publish(twist_msg)
            self.rate.sleep()

        stop_msg = Twist()
        self.velocity_publisher.publish(stop_msg)

    def move_to_goal(self):
        linear_speed = 0.2  # Adjust as needed

        while not rospy.is_shutdown():
            while self.goal_pose is None and not rospy.is_shutdown():
                self.rate.sleep()

            rospy.loginfo("Moving to goal...")
            # self.align_to_goal()
            while self.get_distance_to_goal() > 0.1 and not rospy.is_shutdown():
                angle_to_goal = self.get_angle_to_goal()
                self.align_to_goal()

                # Use PID controller for angular velocity
                angular_speed = self.pid_controller(angle_to_goal)

                twist_msg = Twist()
                twist_msg.linear.x = linear_speed
                twist_msg.angular.z = angular_speed

                self.velocity_publisher.publish(twist_msg)
                self.rate.sleep()

            stop_msg = Twist()
            self.velocity_publisher.publish(stop_msg)

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
