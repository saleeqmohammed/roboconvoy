import rospy
from nav_msgs.msg import OccupancyGrid

def map_callback(msg):
    # Access map data
    map_data = msg.data
    width = msg.info.width
    height = msg.info.height
    resolution =msg.info.resolution
    rospy.loginfo(f'resolution:{resolution}')
    # Process map data here
    pass


rospy.init_node('map_processing_node')
rospy.Subscriber('/map', OccupancyGrid, map_callback)
rospy.spin()
