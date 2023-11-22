import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from geometry_msgs.msg import Pose, PoseArray
from collections import Counter

# Define a class to represent data points with x, y, and additional properties
class DataPoint:
    def __init__(self, x, y, prop1, prop2):
        self.x = x
        self.y = y
        self.prop1 = prop1
        self.prop2 = prop2

# Create a sample dataset with DataPoint objects (replace with your actual data)
data = [DataPoint(x, y, prop1, prop2) for x, y, prop1, prop2 in your_data]







'''
# Plot the clustered data points
plt.scatter(coordinates[:, 0], coordinates[:, 1], c=cluster_labels, cmap='rainbow')
plt.title('K-Means Clustering')
plt.show()
'''
def k_means_estimate(particlecloud: PoseArray):
    data = particlecloud
    # Extract the Euclidean coordinates for clustering
    coordinates = np.array([[point.x, point.y] for point in data])
    # Specify the number of clusters (you can adjust this based on your expectation)
    num_clusters = 2
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)

    # Perform K-Means Clustering
    cluster_labels = kmeans.fit_predict(coordinates)
    # Access other properties for the points within each cluster
    for cluster_label in range(num_clusters):
        cluster_points = [point for point, label in zip(data, cluster_labels) if label == cluster_label]
        print(f'Cluster {cluster_label}:')
        for point in cluster_points:
            print(f'  ({point.x}, {point.y}) - Prop1: {point.prop1}, Prop2: {point.prop2}')