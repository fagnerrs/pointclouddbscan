import csv

import vtk
from numpy import random
import pandas as pd
from HelloKMeans import *
from dbscan1 import *
from Plot3D import *

class VtkPointCloud:

    def __init__(self, zMin=-10.0, zMax=10.0, maxNumPoints=1e6):
        self.maxNumPoints = maxNumPoints
        self.vtkPolyData = vtk.vtkPolyData()

        self.clearPoints()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.vtkPolyData)
        mapper.SetColorModeToDefault()
        mapper.SetScalarRange(zMin, zMax)
        mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(mapper)

    def addPoint(self, point):
        if self.vtkPoints.GetNumberOfPoints() < self.maxNumPoints:
            pointId = self.vtkPoints.InsertNextPoint(point[:])
            self.vtkDepth.InsertNextValue(point[2])
            self.vtkCells.InsertNextCell(1)
            self.vtkCells.InsertCellPoint(pointId)
        else:
            r = random.randint(0, self.maxNumPoints)
            self.vtkPoints.SetPoint(r, point[:])
        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtkDepth.Modified()

    def clearPoints(self):
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkDepth = vtk.vtkDoubleArray()
        self.vtkDepth.SetName('DepthArray')
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepth)
        self.vtkPolyData.GetPointData().SetActiveScalars('DepthArray')

pointCloud = VtkPointCloud()
#for k in range(1000):
#    point = 20*(random.rand(3)-0.5)
#    pointCloud.addPoint(point)

#pointCloud.addPoint([0,0,0])
#pointCloud.addPoint([0,0,0])
#pointCloud.addPoint([0,0,0])
#pointCloud.addPoint([0,0,0])

count = 0

pointsX = []
pointsY = []
pointsZ = []
points = vtk.vtkPoints()

with open('assets/cruzamento02.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar=' ')
  for row in spamreader:

        pointsX.append(float(row[3]))
        pointsY.append(float(row[4]))
        pointsZ.append(float(row[5]))

        pointCloud.addPoint([float(row[3]), float(row[4]), float(row[5])])
        count += 1

points = np.array(points)

points1 = np.array([pointsX, pointsY, pointsZ])

#sample1 = pd.DataFrame({
#  'x': points[:, 0],
#  'y': points[:, 1],
#  'z': points[:, 2]
#})

eps = 0.75
min_points = 10
classifications = dbscan(points1, eps, min_points)


#classPoints = get_class_points(points1, classification, 20)

#plot_bounding_box(classPoints)

plotCloud(points1, classifications)

#kmeans(sample1)

exit()

# Renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(pointCloud.vtkActor)
renderer.SetBackground(.2, .3, .4)
renderer.ResetCamera()

# Render Window
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

# Interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Begin Interaction
renderWindow.Render()
renderWindowInteractor.Start()

print(count)