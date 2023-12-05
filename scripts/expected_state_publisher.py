#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32

def integer_publisher():
    rospy.init_node('integer_publisher_node', anonymous=True)
    pub = rospy.Publisher('/expected_state', Int32, queue_size=10)
    rate = rospy.Rate(1)  # 1 Hz, adjust as needed

    count = 5

    while not rospy.is_shutdown():
        pub.publish(count)
        rospy.loginfo(f'Published: {count}')
        
        rate.sleep()

if __name__ == '__main__':
    try:
        integer_publisher()
    except rospy.ROSInterruptException:
        pass
