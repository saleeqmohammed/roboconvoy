#import matplotlib.pyplot as plt
from geometry_msgs.msg import Pose, PoseArray
from collections import Counter
def euclidean_distance(point1:Pose, point2:Pose):
    return ((point1.position.x - point2.position.x) ** 2 + (point1.position.y - point2.position.y) ** 2) ** 0.5

def region_query(data, point, epsilon):
    neighbors = []
    for i, p in enumerate(data):
        if euclidean_distance(point, p) <= epsilon:
            neighbors.append(i)
    return neighbors

def expand_cluster(data, labels, point_index, cluster_id, epsilon, min_samples):
    seeds = [point_index]
    labels[point_index] = cluster_id

    while seeds:
        current_point_index = seeds.pop(0)
        current_point = data[current_point_index]
        neighbors = region_query(data, current_point, epsilon)

        if len(neighbors) >= min_samples:
            for neighbor_index in neighbors:
                if labels[neighbor_index] == -1 or labels[neighbor_index] == 0:
                    if labels[neighbor_index] == -1:
                        seeds.append(neighbor_index)
                    labels[neighbor_index] = cluster_id

def dbscan(data: PoseArray , epsilon, min_samples):
    n = len(data)
    labels = [0] * n  # 0 represents unclassified, -1 represents noise, and positive integers represent clusters
    cluster_id = 0

    for i in range(n):
        if labels[i] != 0:
            continue

        neighbors = region_query(data, data[i], epsilon)
        if len(neighbors) < min_samples:
            labels[i] = -1  # Mark as noise
        else:
            cluster_id += 1
            expand_cluster(data, labels, i, cluster_id, epsilon, min_samples)

    return labels

def prominent_cluster(epsilon,min_samples,data: PoseArray):

    #cluster data
    cluster_labels = dbscan(data, epsilon, min_samples)

    # Find the most prominent cluster
    cluster_counts = Counter(cluster_labels)
    #print(cluster_labels)
    most_prominent_cluster_label = max(cluster_counts, key=cluster_counts.get)

    # Filter data points belonging to the most prominent cluster
    most_prominent_cluster_data = [data[i] for i, label in enumerate(cluster_labels) if label == most_prominent_cluster_label]
    return most_prominent_cluster_data

def dbscanEstimate(particlecloud:PoseArray):

    estimatedPose = Pose()
    #maximum distance between particles in cluster
    epsilon =3
    #mininum number of particles in a cluster 
    min_particles =2
    #perform a density based spatial clustering based on position
    main_cluster =prominent_cluster(epsilon,min_particles,particlecloud)
    cluster_x =0
    cluster_y =0
    cluster_w =0
    cluster_ori_z =0
    n_cluster =0
    for point in main_cluster:
        cluster_x = cluster_x + point.position.x
        cluster_y = cluster_y + point.position.y
        cluster_w = cluster_w + point.orientation.w
        cluster_ori_z = cluster_ori_z + point.orientation.z
        n_cluster = n_cluster+1
    cluster_x = cluster_x/n_cluster
    cluster_y = cluster_y/n_cluster
    cluster_w = cluster_w/n_cluster
    cluster_ori_z = cluster_ori_z/n_cluster
    estimatedPose.position.x = cluster_x
    estimatedPose.position.y = cluster_y
    estimatedPose.orientation.w = cluster_w
    estimatedPose.orientation.z = cluster_ori_z
    return estimatedPose

        

        


