import math
from statistics import mean,stdev
from geometry_msgs.msg import Pose, PoseArray
def euclidean_function( particle):
        #euclideanDistance = math.sqrt(math.pow(particle.position.x - self.estimatedpose.pose.pose.position.x, 2) + math.pow(particle.position.y - self.estimatedpose.pose.pose.position.y,2))
        euclideanDistance = math.sqrt(math.pow(particle.position.x, 2) + math.pow(particle.position.y,2))
        return euclideanDistance


def particle_clustering(particlePoses):
    """
    Takes the heaviest cluster of particles, and everything that is near it, 
    to recalculate particles and get an estimated pose
    of particles that are within 1 standard deviation rate.
    
    """

    
    euclideanDistances = [] #Initializes a new array to store euclidean distances.

    for pose in particlePoses: #Takes each individual particle in the particle poses array
        euclideanDistances.append(euclidean_function(pose)) #sends each pose to the euclidean function to determine each particle's euclidean distance
                                                                    #and adds to array
    
    meanDistance = mean(euclideanDistances) #Calculates the mean of the distances to use as the center of gaussian
    standardDeviation = stdev(euclideanDistances) #Determines the standard deviation from the mean

    if standardDeviation > 3: #If standard deviation its greater than this, don't consider the particle
        remainingParticlesPoses = [] #creates an array for the new particles
        for pose in particlePoses: # for each particle inside the array of particles
            singleEuclideanDistance = euclidean_function(pose) #sends the particle to get its euclidian distance
            if meanDistance - standardDeviation < singleEuclideanDistance < meanDistance + standardDeviation: # mean - sigma < mean < mean + sigma #boundary of gaussian 
                remainingParticlesPoses.append(pose) #appends the particles to the array that fulfill this condition.
        return particle_clustering(remainingParticlesPoses) #recursive array with new particles, until it returns the robotEstimatedPose std < 3

    else:
        robotEstimatedPose = Pose() #Creates Robot estimated pose

        for pose in particlePoses: #For each  of the remaining particles in the particle cloud, calculate the mean point
            robotEstimatedPose.position.x = robotEstimatedPose.position.x + pose.position.x # This is the new estimated pose in x sum
            robotEstimatedPose.position.y = robotEstimatedPose.position.y + pose.position.y # New estimated pose in y sum
            robotEstimatedPose.orientation.w = robotEstimatedPose.orientation.w + pose.orientation.w # New estimated orientation w sum
            robotEstimatedPose.orientation.z = robotEstimatedPose.orientation.z + pose.orientation.z # New estimated orientation Z sum

        robotEstimatedPose.position.x = robotEstimatedPose.position.x/len(particlePoses) #divides the sum (x) by the number of particle remaining to get mean x
        robotEstimatedPose.position.y = robotEstimatedPose.position.y/len(particlePoses) #divides the sum (y) by the number of particle remaining to get mean y
        robotEstimatedPose.orientation.w = robotEstimatedPose.orientation.w/len(particlePoses) #divides the sum (w) by the number of particle remaining to get mean w
        robotEstimatedPose.orientation.z = robotEstimatedPose.orientation.z/len(particlePoses) #divides the sum (Z) by the number of particle remaining to get mean z
    
        return robotEstimatedPose