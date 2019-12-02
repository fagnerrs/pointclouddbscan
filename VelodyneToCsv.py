reader = vv.getReader()
cloudInfo = reader.GetClientSideObject().GetOutput()
points = cloudInfo.GetPoints()
times = cloudInfo.GetPointData().GetArray("timestamp")
points.GetPoint(10)


reader = vv.smp.GetActiveSource()
cloudInfo = reader.GetClientSideObject().GetOutput()
myintensity = cloudInfo.GetPointData().GetArray("intensity")
query = 'intensity>50'
vv.smp.SelectPoints(query, reader)
vv.smp.Render()
vv.saveCSVCurrentFrameSelection("/Users/fagneroliveira/Documents/PointCloudLibrary/frame_highway.csv")
