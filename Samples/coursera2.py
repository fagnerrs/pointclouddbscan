import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

points = [[1,1, 1], [1, 1, 2], [5, 5, 5], [5, 5, 4]]
points = np.array(points)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(points[:,0], points[:,1], points[:,2],)
plt.show()