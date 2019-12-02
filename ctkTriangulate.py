import vtk
import csv

def main():

  # Create a grid points
  points = vtk.vtkPoints()

  with open('assets/cropped_frame0.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar=' ')
    for row in spamreader:
      points.InsertNextPoint([float(row[3]), float(row[4]), float(row[5])])

    # Add the grid points to a polydata object
    inputPolyData = vtk.vtkPolyData()
    inputPolyData.SetPoints(points)

    # Triangulate the grid points
    delaunay = vtk.vtkDelaunay2D()
    delaunay.SetInputData(inputPolyData)
    delaunay.Update()
    outputPolyData = delaunay.GetOutput()

    bounds= 6*[0.0]
    outputPolyData.GetBounds(bounds)

    # Find min and max z
    minz = bounds[4]
    maxz = bounds[5]

    print("minz: " + str(minz))
    print("maxz: " + str(maxz))

    # Create the color map
    colorLookupTable = vtk.vtkLookupTable()
    colorLookupTable.SetTableRange(minz, maxz)
    colorLookupTable.Build()

    # Generate the colors for each point based on the color map
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")

    print( "There are "+str(outputPolyData.GetNumberOfPoints())+" points.")

    for i in range(0, outputPolyData.GetNumberOfPoints()):
        p= 3*[0.0]
        outputPolyData.GetPoint(i,p)

        dcolor = 3*[0.0]
        colorLookupTable.GetColor(p[2], dcolor);
        print( "dcolor: "
                  + str(dcolor[0]) + " "
                  + str(dcolor[1]) + " "
                  + str(dcolor[2]))
        color=3*[0.0]
        for j in range(0,3):
          color[j] = int(255.0 * dcolor[j])

        print("color: "
               + str(color[0]) + " "
               + str(color[1]) + " "
               + str(color[2]))
        try:
            colors.InsertNextTupleValue(color)
        except AttributeError:
            # For compatibility with new VTK generic data arrays.
            colors.InsertNextTypedTuple(color)


    outputPolyData.GetPointData().SetScalars(colors)

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(outputPolyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Create a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Add the actor to the scene
    renderer.AddActor(actor)
    renderer.SetBackground(.1, .2, .3)

    # Render and interact
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()