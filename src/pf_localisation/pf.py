from geometry_msgs.msg import Pose, PoseArray, Quaternion
from . pf_base import PFLocaliserBase
import math
import rospy
from . import dbscan
from . util import rotateQuaternion, getHeading
from random import gauss, randint, uniform, vonmisesvariate
from . import distance_clustering
from time import time
import numpy as np
from statistics import variance
import pomdp.belief_state_gen as beliefgen


#belief_references = datamanagement.load_object("/home/rahimkhan/catkin_ws/src/roboconvoy_localization/src/pomdp/beliefstate_reference.pickle")
floor_plan = "/home/saleeq/Desktop/new_map_planning_1.png"
state_matrix, centers_dict,belief_ref = beliefgen.get_states(floor_plan)
belief_coordinates = belief_ref.values()
print(belief_coordinates)
#belief_coordinates = list(belief_references.values())  # Use values() to get the tuples

def initialize_particles(direction, coordinates, angle):
        particle_cloud_msg = PoseArray()
        particle_cloud_msg.header.stamp = rospy.Time.now()
        particle_cloud_msg.header.frame_id = "map"  # Adjust the frame_id as needed

        for coordinate in coordinates:
            pose = Pose()
            coordinatex = coordinate[1] - 3
            coordinatey = coordinate[0]- 6.5
            pose.position.x = -coordinatex
            pose.position.y = -coordinatey
            
            pose.position.z = 0.0  # Adjust the z-coordinate as needed
            pose.orientation = Quaternion()  # Assuming no rotation
            pose.orientation=rotateQuaternion(Quaternion(w=1.0),angle)
            particle_cloud_msg.poses.append(pose)
            
        return particle_cloud_msg


class PFLocaliser(PFLocaliserBase):
       
    def __init__(self):
        # ----- Call the superclass constructor
        super(PFLocaliser, self).__init__()
        # ----- Set motion model parameters
        self.ODOM_TRANSLATION_NOISE =0.015
        self.ODOM_DRIFT_NOISE=0.030
        self.ODOM_ROTATION_NOISE=0.022
        # ----- Sensor model parameters
        self.PARTICLECOUNT =100
        self.DOPING_POINT_COUNT = 20     # Number of readings to predict
        self.ENTROPY_LIMIT =12
        self.PARTICLE_RETENTION = 1.00
        #self.particlecloud = self.initialise_particle_cloud(0)
        #--visualisation parameters setting these manually atm since /map_metadata is not subscribed yet
        self.MAP_RESOULUTION = 0.050
        self.MAP_HEIGHT =602*self.MAP_RESOULUTION
        self.MAP_WIDTH =602*self.MAP_RESOULUTION

    def initialise_particle_cloud(self, initialpose:Pose):
        """
        Set particle cloud to initialpose plus noise

        Called whenever an initialpose message is received (to change the
        starting location of the robot), or a new occupancy_map is received.
        self.particlecloud can be initialised here. Initial pose of the robot
        is also set here.
        
        :Args:
            | initialpose: the initial pose estimate
        :Return:
            | (geometry_msgs.msg.PoseArray) poses of the particles
        """
        startingPoses = initialize_particles("up",belief_coordinates,0)
            
        return startingPoses
    def update_particle_cloud(self, scan):
        """
        This should use the supplied laser scan to update the current
        particle cloud. i.e. self.particlecloud should be updated.
        
        :Args:
            | scan (sensor_msgs.msg.LaserScan): laser scan to use for update

         """

        "Initialize Variables"
        weights = [] # Array for storing the weights of each particle
        

        "Scan the weights of each particle"
        for eachParticle in self.particlecloud.poses:
            myPose = Pose() # A pose for each of the particles in the particle cloud
            myPose = eachParticle #assigns that particle to the pose
            weights.append((eachParticle, self.sensor_model.get_weight(scan, eachParticle))) # Creates a tuple with the particle position and weights
        ww =weights[8]
        rospy.loginfo(ww[1])
        



         #updates particle cloud


    def estimate_pose(self):
        #Prediction
        """
        This should calculate and return an updated robot pose estimate based
        on the particle cloud (self.particlecloud).
        
        Create new estimated pose, given particle cloud
        E.g. just average the location and orientation values of each of
        the particles and return this.
        
        Better approximations could be made by doing some simple clustering,
        e.g. taking the average location of half the particles after 
        throwing away any which are outliers

        :Return:
            | (geometry_msgs.msg.Pose) robot's estimated pose.
         """
        #A variety of methods can be adopted here we are implementing positional clustering
        estimatedPose =dbscan.dbscanEstimate(self.particlecloud.poses)
        #estimatedPose = distance_clustering.particle_clustering(self.particlecloud.poses)
        return estimatedPose

        

        

