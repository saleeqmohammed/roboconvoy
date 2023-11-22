#!/usr/bin/env python3
import rospy
from nav_msgs.msg import OccupancyGrid, Odometry

#callback function
def odom_callback(odo: Odometry):
    rospy.loginfo("Position x:{} y{} theta:{}".format(odo.pose.pose.position.x,odo.pose.pose.position.y,odo.pose.pose.orientation.z))
    


if __name__=='__main__':
    rospy.init_node("turtle_pose_sub")
    
    #subsriber needs topic, dtype, callback fun
    sub = rospy.Subscriber("/odom",Odometry , callback=odom_callback)
    
    #log
    rospy.loginfo("subscriber started")

    #create a spin for keeping it alive
    rospy.spin()