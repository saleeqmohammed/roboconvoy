#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import json
import pomdp.belief_state_gen as beliefgen
floor_plan = "/home/saleeq/Desktop/new_map_planning_1.png"
availability_matrix, centers_dict,state_ref = beliefgen.get_states(floor_plan)
def publish_dictionary():
    # Initialize the ROS node
    rospy.init_node('belief_state_referecnce', anonymous=True)

    # Create a publisher for the dictionary on the desired topic
    pub = rospy.Publisher('/belief_state_to_coordinate', String, queue_size=10)

    floor_plan = "/home/saleeq/Desktop/new_map_planning_1.png"
    availability_matrix, centers_dict,state_ref = beliefgen.get_states(floor_plan)
    # Create a dictionary to publish
    dictionary_to_publish = state_ref

    # Rate at which to publish (e.g., 1 Hz)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        # Serialize the dictionary to a JSON string
        json_string = json.dumps(dictionary_to_publish)

        # Publish the JSON string as a std_msgs/String message
        pub.publish(json_string)

        # Sleep to maintain the desired publishing rate
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_dictionary()
    except rospy.ROSInterruptException:
        pass
