#!/usr/bin/env python3

import rospy
from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose
import rospkg
import subprocess
import os

def spawn_turtlebot3(instance_number):
    rospy.init_node('spawn_turtlebot3')

    # Use rospkg to get the path to the turtlebot3_description package
    rospack = rospkg.RosPack()
    package_path = rospack.get_path('turtlebot3_description')

    # Construct the full path to the TurtleBot3 Xacro file
    xacro_path = os.path.join(package_path, "urdf", "turtlebot3_burger.urdf.xacro")

    # Use subprocess to call xacro and generate the URDF
    xacro_command = ["xacro", xacro_path]
    urdf_process = subprocess.Popen(xacro_command, stdout=subprocess.PIPE)
    model_xml = urdf_process.communicate()[0]

    # Convert bytes to string
    model_xml_str = model_xml.decode('utf-8')

    spawn_model = rospy.ServiceProxy('/gazebo/spawn_urdf_model', SpawnModel)
    locations=[(-2,-5,0),(2,-5,0),(0,0,0)]
    turtlebot3_pose = Pose()
    lock=locations[instance_number]
    turtlebot3_pose.position.x =lock[0]  # Adjust the x-coordinate based on the instance number
    turtlebot3_pose.position.y =lock[1]
    turtlebot3_pose.position.z =lock[2]

    model_name = "turtlebot3_" + str(instance_number)

    try:
        spawn_model(model_name, model_xml_str, "robot_namespace", turtlebot3_pose, "world")
        rospy.loginfo("TurtleBot3 instance {} spawned successfully!".format(instance_number))
    except rospy.ServiceException as e:
        rospy.logerr("Error while spawning TurtleBot3 instance {}: {}".format(instance_number, str(e)))

if __name__ == '__main__':
    num_instances = 3  # Change this to the desired number of TurtleBot3 instances

    for i in range(num_instances):
        try:
            spawn_turtlebot3(i)
        except rospy.ROSInterruptException:
            pass
 