#http://benalexkeen.com/k-means-clustering-in-python/

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import copy

## Assignment Stage
# 1. Calcula a distância cada ponto P e centroid K
# 2. Associa os pontos P aos centroids K com base na menor distância
# 3. Associa cor a cada um dos centrois
def assignment(sample, centroids, colmap):
    for i in centroids.keys():
        # sqrt((x1 - x2)^2 - (y1 - y2)^2)
        sample['distance_from_{}'.format(i)] = (
            np.sqrt(
              (sample['x'] - centroids[i][0]) ** 2
              + (sample['y'] - centroids[i][1]) ** 2
              + (sample['z'] - centroids[i][2]) ** 2
            )
        )

    centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]

    #idmin - retorna index do minimo valor da coluna
    sample['closest'] = sample.loc[:, centroid_distance_cols].idxmin(axis=1)

    #lstrip - remove string
    sample['closest'] = sample['closest'].map(lambda x: int(x.lstrip('distance_from_')))

    # associa cor
    sample['color'] = sample['closest'].map(lambda x: colmap[x])

    return sample


# Update centroid positions
# Selection pontos associados a cada centroid
# Calcula mean dos pontos
# Atualiza centroids
def update(k, centroids, sample):
  for i in centroids.keys():
    centroids[i][0] = np.mean(sample[sample['closest'] == i]['x'])
    centroids[i][1] = np.mean(sample[sample['closest'] == i]['y'])
    centroids[i][2] = np.mean(sample[sample['closest'] == i]['z'])

    print(*centroids[i])

  return k

def scan_neighbords(data, neighbors, epsilon, minPts):
  for pos in range(len(neighbors)):



    neighbors = get_neighbors(data, data, epsilon)

    if len(neighbors) >= minPts:
      scan_neighbords(neighbors, epsilon, minPts)

def dbscan(data, epsilon, minPts):

  for pos in range(len(data['x'])):

    point = data['x'][pos]

    neighbors = get_neighbors(point, data, epsilon)

    if len(neighbors) >= minPts:
      scan_neighbords(data, neighbors, epsilon, minPts)
    #else:
     # data['noise'][pos] = 1



  #print(data['noise'])


def get_neighbors(point, data, epsilon):
  items = []
  for pos in range(len(data['x'])):
    distance = np.sqrt(
                  (point[0] - data['x'][pos][0]) ** 2
                + (point[1] - data['x'][pos][1]) ** 2
                + (point[2] - data['x'][pos][2]) ** 2
              )

    #print('origin ', point)
    #print('distance', distance)

    if distance < epsilon:
      items.append(pos)

  return items

data = pd.DataFrame({
  'x': [[1, 1, 1], [2, 2, 2], [5, 5, 5], [10, 10, 10]],
  'noise': [0, 0, 0, 0],
  'core': [0, 0, 0, 0],
  'border': [0, 0, 0, 0]
})

data1 = pd.DataFrame({
  'x': [1, 2, 5, 10],
  'y': [1, 2, 5, 10],
  'z': [1, 2, 5, 10],
  'noise': [0, 0, 0, 0],
  'core': [0, 0, 0, 0],
  'border': [0, 0, 0, 0]
})

epsilon = 3
minPts = 2

dbscan(data, epsilon, minPts)
