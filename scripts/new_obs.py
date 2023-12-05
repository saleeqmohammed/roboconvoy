#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist, PoseStamped, Pose,PoseArray
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from math import atan2, sqrt
from std_msgs.msg import String, Int32
import json

def get_distance_from_pose_and_coordinate(pose, coordinate):
    pose_x = pose.position.x
    pose_y = pose.position.y
    coordinate_x = 6.5+coordinate[0]
    coordinate_y = 3+coordinate[1]

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
        self.state_publisher = rospy.Publisher('/state', Int32, queue_size=10)
        self.pose_array_publisher = rospy.Publisher('/pose_array', PoseArray, queue_size=10)
        self.odom_subscriber = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.belief_subscriber = rospy.Subscribeexpected_stater('/belief_state_to_coordinate', String, self.belief_callback)
        self.rate = rospy.Rate(10)  # 10 Hz
        self.current_pose = None
        self.belief_state_dict = None

    def belief_callback(self, belief_dict):
        self.belief_state_dict = json.loads(belief_dict.data)

    def odom_callback(self, odom_msg):
        self.current_pose = odom_msg.pose.pose

    def publish_pose_array(self, coordinates):
        pose_array_msg = PoseArray()
        pose_array_msg.header.stamp = rospy.Time.now()
        pose_array_msg.header.frame_id = "map"  # Assuming the frame_id is "map", adjust if needed
        for coordinate in coordinates:
            pose = Pose()
            pose.position.x = 6.5 + coordinate[0]
            pose.position.y = 3 + coordinate[1]
            pose.orientation.w = 1.0  # Quaternion for 0 angle
            pose_array_msg.poses.append(pose)
        self.pose_array_publisher.publish(pose_array_msg)

    def find_state(self):
        while not rospy.is_shutdown():
            while self.current_pose is not None and self.belief_state_dict is not None:
                belief_dict = self.belief_state_dict
                coordinates_to_states = list(belief_dict.values())
                min_coordinate = coordinates_to_states[0]
                for coordinate in coordinates_to_states:
                    if get_distance_from_pose_and_coordinate(self.current_pose, coordinate) < get_distance_from_pose_and_coordinate(self.current_pose, min_coordinate):
                        min_coordinate = coordinate
                state = get_key_by_value(self.belief_state_dict, min_coordinate)
                rospy.loginfo(f'state: {state} , coordinate: {min_coordinate}')
                self.state_publisher.publish(Int32(state))
                self.publish_pose_array(coordinates_to_states)
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



