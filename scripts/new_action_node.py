#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool, Int32

class ExampleNode:
    def __init__(self):
        rospy.init_node('example_node', anonymous=True)

        self.boolean_status = False
        self.integer_value = 0

        # Subscriber to boolean status
        rospy.Subscriber('/moved_status', Bool, self.boolean_status_callback)

        # Publisher for integer topic
        self.integer_pub = rospy.Publisher('/expected_state', Int32, queue_size=10)

        # Run the main loop
        self.run()

    def boolean_status_callback(self, msg):
        self.boolean_status = msg.data

    def run(self):
        rate = rospy.Rate(10)  # 10 Hz
        while not rospy.is_shutdown():
            if not self.boolean_status:
                # Run your function here
                #self.run_function()

                # Publish the current integer value
                self.integer_pub.publish(self.integer_value)
            else:
                # Boolean status is true, update the integer value
                self.integer_value -=1
                self.integer_pub.publish(self.integer_value)

            rate.sleep()

    def run_function(self):
        # Replace this with your own function to run while boolean status is false
        print("Running function...")

if __name__ == '__main__':
    try:
        example_node = ExampleNode()
    except rospy.ROSInterruptException:
        pass
