import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

UNCLASSIFIED = False
NOISE = None

def _dist(p, q):
  return np.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2)

def _eps_neighborhood(p, q, eps):
  return _dist(p, q) < eps


def _region_query(pointcloud, point_id, eps):
  n_points = pointcloud.shape[1]
  seeds = []
  for i in range(0, n_points):
    if _eps_neighborhood(pointcloud[:, point_id], pointcloud[:, i], eps):
      seeds.append(i)
  return seeds


def _expand_cluster(pointcloud, classifications, point_id, cluster_id, eps, min_points):
  seeds = _region_query(pointcloud, point_id, eps)
  if len(seeds) < min_points:
    classifications[point_id] = NOISE
    return False
  else:
    classifications[point_id] = cluster_id
    for seed_id in seeds:
      classifications[seed_id] = cluster_id

    while len(seeds) > 0:
      current_point = seeds[0]
      results = _region_query(pointcloud, current_point, eps)
      if len(results) >= min_points:
        for i in range(0, len(results)):
          result_point = results[i]
          if classifications[result_point] == UNCLASSIFIED or classifications[result_point] == NOISE:
            if classifications[result_point] == UNCLASSIFIED:
              seeds.append(result_point)

            classifications[result_point] = cluster_id
      seeds = seeds[1:]
    return True


def dbscan(pointcloud, eps, min_points):
  cluster_id = 1
  n_points = pointcloud.shape[1]
  classifications = [UNCLASSIFIED] * n_points
  for point_id in range(0, n_points):
    point = pointcloud[:, point_id]
    if classifications[point_id] == UNCLASSIFIED:
      if _expand_cluster(pointcloud, classifications, point_id, cluster_id, eps, min_points):
        cluster_id = cluster_id + 1

  return classifications

def getIntClasses(classes):
  intClasses = []
  for i in classes:
    if i is not None:
      intClasses.append(i)

  return intClasses

def get_class_points(point_cloud, classes, index):

  pointsX = []
  pointsY = []
  pointsZ = []

  for i in range(len(classes)):
    if classes[i] == index:
      pointsX.append(point_cloud[0][i])
      pointsY.append(point_cloud[1][i])
      pointsZ.append(point_cloud[2][i])

  return np.array([pointsX, pointsY, pointsZ])