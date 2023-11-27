#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import pygame

# Initialize Pygame
pygame.init()

# Set the width and height of the screen (width, height).
size = (300, 200)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("TurtleBot3 Gamepad Control")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize ROS node
rospy.init_node("turtlebot3_gamepad_control")
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

# Function to map key events to velocities
def map_keys_to_velocities(keys):
    twist = Twist()
    linear_vel = 0.2  # Adjust as needed
    angular_vel = 1.0  # Adjust as needed

    if keys[pygame.K_UP]:
        twist.linear.x = linear_vel
    if keys[pygame.K_DOWN]:
        twist.linear.x = -linear_vel
    if keys[pygame.K_LEFT]:
        twist.angular.z = angular_vel
    if keys[pygame.K_RIGHT]:
        twist.angular.z = -angular_vel
    if keys[pygame.K_SPACE]:
        twist.linear.x = 0.0
        twist.angular.z = 0.0
    if keys[pygame.K_s]:
        twist.linear.x = -linear_vel

    return twist

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here

    # --- Getting the state of all keys
    keys = pygame.key.get_pressed()

    # --- Update the robot velocity based on key events
    cmd_vel = map_keys_to_velocities(keys)

    # --- Publish the Twist message
    pub.publish(cmd_vel)

    # --- Drawing code goes here

    # --- Limit to 30 frames per second
    clock.tick(30)

# Close the window and quit.
pygame.quit()
