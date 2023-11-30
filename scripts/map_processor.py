#!/usr/bin/env python

import rospy
from nav_msgs.msg import OccupancyGrid
import cv2
from itertools import chain
def generate_mapdata(path_to_image):
    img_data = cv2.imread(path_to_image,cv2.IMREAD_GRAYSCALE)
    img_size =img_data.shape
    #cv2.imshow("read map",img_data)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    m_data = list(chain(*img_data))
    return [m_data,img_size[1],img_size[0]]
def publish_map():
    rospy.init_node('map_publisher_node', anonymous=True)
    map_pub = rospy.Publisher('/custom_map', OccupancyGrid, queue_size=10)

    rate = rospy.Rate(1)  # Publish at 1 Hz (adjust as needed)

    # Define your map dimensions and data (example map)
    #width = 10
    #height = 10
    resolution = 1.0  # meters per cell
    generate_mapdata("/home/saleeq/catkin_ws/src/roboconvoy/map_3d_markers.pgm")
    map_data = [0] * (width * height)  # Initialize with zeros (free space)

    # Set some occupied cells in the map
    map_data[5 * width + 5] = 100  # Example: Cell at row 5, column 5 is occupied

    while not rospy.is_shutdown():
        # Create OccupancyGrid message
        map_msg = OccupancyGrid()
        map_msg.header.stamp = rospy.Time.now()
        map_msg.header.frame_id = "map"
        map_msg.info.width = width
        map_msg.info.height = height
        map_msg.info.resolution = resolution
        map_msg.info.origin.position.x = 0.0
        map_msg.info.origin.position.y = 0.0
        map_msg.info.origin.position.z = 0.0
        map_msg.info.origin.orientation.x = 0.0
        map_msg.info.origin.orientation.y = 0.0
        map_msg.info.origin.orientation.z = 0.0
        map_msg.info.origin.orientation.w = 1.0
        map_msg.data = map_data

        # Publish the map
        map_pub.publish(map_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_map()
    except rospy.ROSInterruptException:
        pass
