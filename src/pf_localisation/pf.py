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
        startingPoses = PoseArray()
        #create x and y coordinates of possible posses in a normal distribution around inital position
        initialPositions_x =[gauss(initialpose.pose.pose.position.x,self.MAP_WIDTH/8) for _ in range(self.PARTICLECOUNT)]
        initialPositions_y =[gauss(initialpose.pose.pose.position.y,self.MAP_HEIGHT/8) for _ in range(self.PARTICLECOUNT)]
        #create random uniform probability angles
        initialAngles = [vonmisesvariate(0,0) for x in range(self.PARTICLECOUNT)]
        for _ in range(self.PARTICLECOUNT):
            currPose = Pose()
            currPose.position.x = initialPositions_x[_]
            currPose.position.y = initialPositions_y[_]
            currPose.orientation=rotateQuaternion(Quaternion(w=1.0),initialAngles[_])
            startingPoses.poses.append(currPose)
            
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
        
        sortedWeights = sorted(weights, key=lambda higherWeights: higherWeights[1], reverse=True) # Puts higher weight particles at top of array to guarantee copies
        heaviestParticles = sortedWeights[0:int(self.PARTICLECOUNT * self.PARTICLE_RETENTION)] #Takes the % heaviest particles in a new array

        weightSum = sum(higherWeights[1] for higherWeights in heaviestParticles) #Does the sum of weights for top particles


        " Particles to add via new random position generation "
        dopingPoses = PoseArray() #The Array we are going to return for the cloud
        width = self.occupancy_map.info.width #The width of the map, so particles only span inside of the width
        height = self.occupancy_map.info.height #The height of the map so particle only span inside the heigh of the map
        resolution = self.occupancy_map.info.resolution #gives the resolution of the map
        dopingPoints =self.DOPING_POINT_COUNT# cloudPoints * (1-self.PARTICLE_RETENTION) # Is the number of cloud points we are now randomly determining
        appendedParticles = 0 # To check that the remaining cloudpoints have been added

        while appendedParticles < dopingPoints:
            myPose = Pose() #creates a pose variable, once per cycle to not cause problem when appending
            random_angle = vonmisesvariate(0,0) # generates a random angle between 0 to 2pi
            random_x = randint(0,width-1)# generates a random position around center of map 
            random_y = randint(0,height-1) # generates a random position around center of map
            myPose.position.x = random_x * resolution #Multiplies by the resolution of the map so the correct x position is obtained
            myPose.position.y = random_y * resolution #Multiplies by the resolution of the map so the correct y position is obtained
            myPose.orientation = rotateQuaternion(Quaternion(w=1.0),random_angle) #rotates from default quaternion into new angle

            if self.occupancy_map.data[random_x + random_y * width] == 0: # Verifies that the particle is created in a white space
                dopingPoses.poses.append(myPose) #Adds the particle to an array.
                appendedParticles += 1 #Ready to append the next particle
            



        """ Resampling of topWeight Particles"""
        # ------ Cumulative Distribution initialization
        cumulativeDistribution = [] #Initializes the cumulative distribution array
        accumulatedWeight = 0 #The initial weight of the particle

        for (particle, weight) in heaviestParticles: #Heaviest particle array has particle data, and weight data, this was already sorted before, created this to make new array
            cumulativeDistribution.append((particle, accumulatedWeight + weight/weightSum)) # Appends the particle info, and the accumulated weight to create cumulative weight distribution. 
            accumulatedWeight = accumulatedWeight + weight/weightSum #Accumulate weights 
        
        threshold = uniform(0,math.pow(len(heaviestParticles),-1)) #Creates uniform distribution for the threshold to update particles
        skip = 0 # variable for while
        arrayPoses = PoseArray() #creates an array of poses to store poses
        induvidual_probabilities =[point[1] for point in weights]
        probabilitySum = sum(induvidual_probabilities)
        probabilities =[p/probabilitySum for p in induvidual_probabilities]
        #entropy = -np.dot(probabilities,np.log(probabilities))/np.log(len(probabilities))
        cloud_varience =variance(probabilities)
        N_particles =5.5*(cloud_varience*10**8)+50
        if N_particles < 100:
            N_particles = 100
        elif N_particles > 800:
            N_particles =800
        self.PARTICLECOUNT = N_particles
        N_dops =-0.278*(cloud_varience*10**8)+19.83
        if N_dops <10:
            N_dops=10
        elif N_dops > 20:
            N_dops=20
        self.DOPING_POINT_COUNT =N_dops
        #self.PARTICLECOUNT = f(variance)
        #self.DOPING_POINT_COUNT =g(variance)
        rospy.loginfo("Variance :{}".format(cloud_varience))
        for points in range(0, len(heaviestParticles)): #starts updating threshold and storing positions  of heaviest particles
            while threshold > cumulativeDistribution[skip][1]:
                skip += 1 
            
            myPose = Pose() #stores the new pose
            myPose.position.x = cumulativeDistribution[skip][0].position.x + gauss(0,self.ODOM_TRANSLATION_NOISE ) #stores position x
            myPose.position.y = cumulativeDistribution[skip][0].position.y + gauss(0,self.ODOM_DRIFT_NOISE ) #stores position y
            myPose.orientation = rotateQuaternion(Quaternion(w=1.0), getHeading(cumulativeDistribution[skip][0].orientation) + 
                            gauss(0, self.ODOM_ROTATION_NOISE)) #stores orientation

            arrayPoses.poses.append(myPose) #appends the pose
            threshold = threshold + math.pow(len(heaviestParticles),-1) #continues updating the threshold


        modifiedPosesArray = arrayPoses #stores the array in the modified array
        modifiedPosesArray.poses = modifiedPosesArray.poses + dopingPoses.poses #combines both array poses


        self.particlecloud = modifiedPosesArray #updates particle cloud


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

        

        

