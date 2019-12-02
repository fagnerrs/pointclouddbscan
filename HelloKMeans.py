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


def kmeans(sample):

  colmap = {1: 'r', 2: 'g', 3: 'b'}
  k = 3

  # Get max value if each axis
  maxX = sample['x'].max()
  maxY = sample['y'].max()
  maxZ = sample['z'].max()

  print(len( sample['x']))
  print(len( sample['y']))
  print(maxZ)

  # Random selection of centroids
  centroids = {
    i + 1: [np.random.uniform(0, maxX), np.random.uniform(0, maxY), np.random.uniform(0, maxZ)] for i in range(k)
  }

  # Assign values
  sample = assignment(sample, centroids, colmap)

  ## Repeat Assigment Stage
  centroids = update(centroids, centroids, sample)
  sample = assignment(sample, centroids, colmap)

  # Plot results
  fig = plt.figure(figsize=(5, 5))
  ax = fig.add_subplot(111, projection='3d')

  ax.scatter(sample['x'], sample['y'], sample['z'], color=sample['color'], alpha=0.5, edgecolor='k')
  for i in centroids.keys():
      ax.scatter(*centroids[i], color=colmap[i])

  # Show first mean
  plt.show()

  # Continue until all assigned categories don't change any more
  while True:
      closest_centroids = sample['closest'].copy(deep=True)

      # Atualiza centroid K: MEAN
      centroids = update(centroids, centroids, sample)

      # Reassocia novo centroid K aos pontos P
      sample = assignment(sample, centroids, colmap)

      # Caso centroid não mude, FINISH
      if closest_centroids.equals(sample['closest']):
          break

  fig = plt.figure(figsize=(5, 5))
  ax = fig.add_subplot(111, projection='3d')

  ax.scatter(sample['x'], sample['y'], sample['z'], color=sample['color'], alpha=0.5, edgecolor='k')
  #for i in centroids.keys():
  #    plt.scatter(*centroids[i], color=colmap[i])

  plt.show()

sample1 = pd.DataFrame({
  'x': [1, 2, 10, 20],
  'y': [1, 2, 10, 20],
  'z': [1, 2, 10, 20]
})

sample2 = pd.DataFrame({
    'x': [12, 20, 28, 18, 29, 33, 24, 45, 45, 52, 51, 52, 55, 53, 55, 61, 64, 69, 72, 250, 500],
    'y': [39, 36, 30, 52, 54, 46, 55, 59, 63, 70, 66, 63, 58, 23, 14, 8, 19, 7, 24, 250, 500],
    'z': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 250, 500 ]
})

#kmeans(sample2)
