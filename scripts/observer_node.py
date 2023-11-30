import rospy
import pf_localisation.sensor_model
import datamanagement
from geometry_msgs.msg import Pose, PoseArray, Quaternion

belief_references = datamanagement.load_object("/home/saleeq/catkin_ws/src/roboconvoy/src/pomdp/beliefstate_reference.pickle")
belief_coordinates = belief_references.keys()
def initialize_expexted_observations(direction,coordinate):
    
    
    pass
initialize_expexted_observations("up",belief_coordinates)