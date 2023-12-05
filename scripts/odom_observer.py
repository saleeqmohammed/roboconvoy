#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist, PoseStamped, Pose, PoseArray, Quaternion
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sqrt
from std_msgs.msg import String, Int32
import json


def initialize_particles(coordinates):
        particle_cloud_msg = PoseArray()
        particle_cloud_msg.header.stamp = rospy.Time.now()
        particle_cloud_msg.header.frame_id = "map"  # Adjust the frame_id as needed

        for coordinate in coordinates:
            pose = Pose()
            coordinatex = coordinate[0] - 3
            coordinatey = coordinate[1]- 6.5
            pose.position.x = -coordinatex
            pose.position.y = -coordinatey
            
            pose.position.z = 0.0  # Adjust the z-coordinate as needed
            pose.orientation = Quaternion()  # Assuming no rotation
            pose.orientation=Quaternion(w=1.0)
            particle_cloud_msg.poses.append(pose)
            
        return particle_cloud_msg

def get_distance_from_pose_and_coordinate(pose, coordinate):
    pose_x = pose.position.x
    pose_y = pose.position.y
    coordinate_x = -(coordinate[0] - 3)
    coordinate_y = -(coordinate[1]- 6.5)


    # Transformed point=(0.00167×x−3.00167,−0.00532×y+6.06383)
    #coordinate_x = 0.00167 * coordinate_x - 3.00167
    #coordinate_y = -0.00532 * coordinate_y + 6.06383
    dist = sqrt(((coordinate_x - pose_x) ** 2) + ((coordinate_y - pose_y) ** 2))
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
        self.state_publisher = rospy.Publisher('/curr_state', Int32, queue_size=10)
        self.odom_subscriber = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.pose_array_publisher = rospy.Publisher('/pose_sarray', PoseArray, queue_size=10)
        self.belief_subscriber = rospy.Subscriber('/belief_state_to_coordinate', String, self.belief_callback)
        self.rate = rospy.Rate(10)  # 10 Hz
        self.current_pose = None
        self.expected_pose = None
        self.belief_state_dict = None
        self.bel_state_coords=None

    def belief_callback(self, belief_dict):
        self.belief_state_dict = json.loads(belief_dict.data)
        
        self.pose_array_publisher.publish(initialize_particles(list(self.belief_state_dict.values())))
        # rospy.loginfo(belif_state_dict)

    def odom_callback(self, odom_msg):
        self.current_pose = odom_msg.pose.pose


    def find_state(self):
        while not rospy.is_shutdown():
            while self.current_pose is not None and self.belief_state_dict is not None:
                belief_dict = self.belief_state_dict
                self.bel_state_coords =list(belief_dict.values())
                coordinates_to_states = list(belief_dict.values())
                min_coordinate = coordinates_to_states[0]
                for coordinate in coordinates_to_states:
                    if get_distance_from_pose_and_coordinate(self.current_pose, coordinate) < get_distance_from_pose_and_coordinate(self.current_pose, min_coordinate):
                        min_coordinate = coordinate
                state = get_key_by_value(self.belief_state_dict, min_coordinate)
                #rospy.loginfo(f'state: {state} , coordinate: {min_coordinate}')
                
                self.state_publisher.publish(int(state))  # Added state as argument
                self.rate.sleep()

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
