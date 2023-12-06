#!/usr/bin/env python3

import rospy
from std_msgs.msg import Bool, Int32

def calculate_value(input_list):
        # Replace this with your actual calculation logic
        for value in input_list:
            yield value

class MyNode:
    def __init__(self):
        rospy.init_node('my_node', anonymous=False)
        
        self.flag = False
        self.previous_value = 90
        self.rate = rospy.Rate(1)  # 1 Hz, adjust as needed
        self.input_list =[81,82,83,84,85,70,55]
        # Subscribe to the boolean flag topic
        rospy.Subscriber('moved_status', Bool, self.flag_callback)

        # Create a publisher for the calculated value
        self.value_publisher = rospy.Publisher('expected_state', Int32, queue_size=10)
        self.generator = calculate_value(self.input_list)

    def flag_callback(self, msg):
        # Update flag when a new message is received
        self.flag = msg.data


        
    def run(self):
        while not rospy.is_shutdown():
            if self.flag:
                # If flag is true, calculate and publish new value
                rospy.loginfo("next called!")
                new_value = next(self.generator)
                self.value_publisher.publish(new_value)
                self.previous_value = new_value
            else:
                # If flag is false, keep publishing previous value
                self.value_publisher.publish(self.previous_value)

            self.rate.sleep()

if __name__ == '__main__':
    try:
        node = MyNode()
        node.run()
    except rospy.ROSInterruptException:
        pass
