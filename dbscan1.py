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


def _region_query(m, point_id, eps):
  n_points = m.shape[1]
  seeds = []
  for i in range(0, n_points):
    if _eps_neighborhood(m[:, point_id], m[:, i], eps):
      seeds.append(i)
  return seeds


def _expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
  seeds = _region_query(m, point_id, eps)
  if len(seeds) < min_points:
    classifications[point_id] = NOISE
    return False
  else:
    classifications[point_id] = cluster_id
    for seed_id in seeds:
      classifications[seed_id] = cluster_id

    while len(seeds) > 0:
      current_point = seeds[0]
      results = _region_query(m, current_point, eps)
      if len(results) >= min_points:
        for i in range(0, len(results)):
          result_point = results[i]
          if classifications[result_point] == UNCLASSIFIED or \
            classifications[result_point] == NOISE:
            if classifications[result_point] == UNCLASSIFIED:
              seeds.append(result_point)
            classifications[result_point] = cluster_id
      seeds = seeds[1:]
    return True


def dbscan(m, eps, min_points):
  cluster_id = 1
  n_points = m.shape[1]
  classifications = [UNCLASSIFIED] * n_points
  for point_id in range(0, n_points):
    point = m[:, point_id]
    if classifications[point_id] == UNCLASSIFIED:
      if _expand_cluster(m, classifications, point_id, cluster_id, eps, min_points):
        cluster_id = cluster_id + 1

  print(classifications)

  return classifications

#m = np.array([[1, 1.2, 0.8, 3.7, 3.9, 3.6, 10], [1.1, 0.8, 1, 4, 3.9, 4.1, 10], [1.1, 0.8, 1, 4, 3.9, 4.1, 10]])

#m = np.array([[12, 20, 28, 18, 29, 33, 24, 45, 45, 52, 51, 52, 55, 53, 55, 61, 64, 69, 72],
              #[39, 36, 30, 52, 54, 46, 55, 59, 63, 70, 66, 63, 58, 23, 14, 8, 19, 7, 24],
              #[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

#eps = 7
#min_points = 2
#dbscan(m, eps, min_points)