#!/bin/bash

# Install TurtleBot3 packages
sudo apt-get install ros-noetic-turtlebot3*

# Set up TurtleBot3 model
echo "export TURTLEBOT3_MODEL=waffle_pi" >> ~/.bashrc
source ~/.bashrc

# Install Gazebo
sudo apt-get install ros-noetic-gazebo-ros-pkgs ros-noetic-gazebo-ros-control

# Clone TurtleBot3 simulation packages
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git

# Build the workspace
cd ~/catkin_ws
catkin_make

# Source the setup file
source devel/setup.bash

# Launch Gazebo with TurtleBot3
roslaunch turtlebot3_gazebo turtlebot3_world.launch
echo "export TURTLEBOT3_MODEL=burger" >> ~/.bashrc
sudo apt install python3-pip
pip3 install pygame