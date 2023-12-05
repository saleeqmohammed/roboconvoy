#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist, PoseStamped, Pose, Quaternion
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sqrt
from std_msgs.msg import String, Int32,Bool
import json
from pf_localisation.util import rotateQuaternion, getHeading

class MoveRobot:
    def __init__(self):
        rospy.init_node('move_robot_node', anonymous=True)
        self.curr_state = 95
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_subscriber = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.current_pose_subscriber = rospy.Subscriber('/curr_state',Int32,self.curr_state_callback)
        self.expected_pose_subscriber =rospy.Subscriber('/expected_state',Int32,self.goal_callback)
        self.belief_subscriber = rospy.Subscriber('/belief_state_to_coordinate', String, self.belief_callback)
        self.status_publisher = rospy.Publisher("/moved_status",Bool,queue_size=10)
        #self.goal_subscriber = rospy.Subscriber('/move_base_simple/goal', PoseStamped, self.goal_callback)
        self.rate = rospy.Rate(10)  # 10 Hz
        self.current_pose = None
        self.goal_pose = None
        self.curr_state =None
        self.belief_state_dict =None
        self.belief_state_coords =None
        self.move_completed =False
        self.expected_state = None
    def curr_state_callback(self,msg):
        self.curr_state = msg.data
    def belief_callback(self, belief_dict):
        self.belief_state_dict = json.loads(belief_dict.data)
        self.belief_state_coords = list(self.belief_state_dict.values())


    def odom_callback(self, odom_msg):
        self.current_pose = odom_msg.pose.pose
    def goal_callback(self, expected_state):
        if self.curr_state != expected_state.data:
            self.move_completed = False
            self.expected_state = expected_state.data
            goal_pose = Pose()
            #print(expected_state.data)
            coordinate = self.belief_state_coords[expected_state.data]
            coordinate_x = -(coordinate[0] - 3)
            coordinate_y = -(coordinate[1]- 6.5)
            goal_pose.position.x = coordinate_x
            goal_pose.position.y = coordinate_y
            curr_coordinates =self.belief_state_coords[self.curr_state]
            curr_coordinates_yy =-(curr_coordinates[1]- 6.5)
            curr_coordinates_xx =-(curr_coordinates[0]- 3)
            angle =atan2( coordinate_y-curr_coordinates_yy, coordinate_x-curr_coordinates_xx)
            goal_pose.orientation = rotateQuaternion(Quaternion(w=1.0),angle)
        else:
            self.move_completed=True
            #rospy.loginfo(f'current state{self.curr_state.data} expected state:{self.expected_state.data}')
        self.goal_pose = goal_pose

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

            rospy.loginfo(f'Moving to state {self.expected_state}')
            #self.align_to_goal()
            while self.get_distance_to_goal() > 0.1 and not rospy.is_shutdown():
                angle_to_goal = self.get_angle_to_goal()
                self.align_to_goal()
                twist_msg = Twist()
                twist_msg.linear.x = linear_speed
                twist_msg.angular.z = angular_speed * angle_to_goal

                self.velocity_publisher.publish(twist_msg)
                self.status_publisher.publish(self.move_completed)
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
