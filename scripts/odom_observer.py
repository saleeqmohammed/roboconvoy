#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist, PoseStamped , Pose
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sqrt
from std_msgs.msg import String,Int32
import json


def get_distane_form_pose_and_coordinate(pose,coordinate):
    pose_x = pose.position.x
    pose_y = pose.position.y
    coordinate_x = coordinate[0]
    coordinate_y = coordinate[1]
    
    dist = sqrt(((coordinate_x-pose_x)**2 )+((coordinate_y-pose_y)**2))
    return dist
def get_key_by_value(my_dict, target_value):
    for key, value in my_dict.items():
        if value == target_value:
            return key
    # If the value is not found, you may want to handle this case accordingly
    return None
class Observer:
    def __init__(self):
        rospy.init_node('state_observer_node', anonymous=True)
        self.state_publisher = rospy.Publisher('/state',Int32,queue_size=10)
        self.odom_subscriber = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.belief_subscriber = rospy.Subscriber('/belief_state_to_coordinate',String,self.belief_callback)
        self.rate = rospy.Rate(10)  # 10 Hz
        self.current_pose = None
        self.expected_pose = None
        self.belief_state_dict = None

    def belief_callback(self,belief_dict):
        self.belief_state_dict = json.loads(belief_dict.data)
        #rospy.loginfo(belif_state_dict)

    def odom_callback(self, odom_msg):
        self.current_pose = odom_msg.pose.pose

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
    def find_state(self):
        while not rospy.is_shutdown():
            while self.current_pose is not None and self.belief_state_dict is not None:
                belief_dict = self.belief_state_dict
                coordinates_to_states = list(belief_dict.values())
                min_coordinate = coordinates_to_states[0]
                for coordinate in coordinates_to_states:
                    if get_distane_form_pose_and_coordinate(self.current_pose,coordinate) < get_distane_form_pose_and_coordinate(self.current_pose,min_coordinate):
                        min_coordinate = coordinate
                state =get_key_by_value(self.belief_state_dict,min_coordinate)
                rospy.loginfo(f'state: {state} , coordinate: {min_coordinate}')
                self.state_publisher.publish()


            


    def run(self):
        try:
            self.find_state()
        except rospy.ROSInterruptException:
            pass

if __name__ == '__main__':
    try:
        observer = Observer()
        observer.run()
    except rospy.ROSInterruptException:
        pass
