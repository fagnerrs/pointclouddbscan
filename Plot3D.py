import plotly
import plotly.graph_objs as go
import numpy as np

def plotCloud(lidar_pointcloud, classifications):  # Code taken from StackOverFlow, sadly forgot the link

  colmap = []
  for i in range(len(lidar_pointcloud[0])):
    colmap.append('#%06X' % np.random.randint(0, 0xFFFFFF))

  colors = [colmap[v] if v is not None else '#000000' for v in classifications]

  # Configure the trace.
  trace = go.Scatter3d(
    x=lidar_pointcloud[0],
    y=lidar_pointcloud[1],
    z=lidar_pointcloud[2],
    mode='markers',
    marker={
      'size': 1,
      'opacity': 0.8,
      'color': colors
    }
  )

  # Configure the layout.
  layout = go.Layout(
    margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
    scene=dict(
      xaxis=dict(showgrid = False, title="x", range=[-100, 100], backgroundcolor="rgb(0, 0, 0)"),
      yaxis=dict(showgrid = False, title="y", range=[-100, 100], backgroundcolor="rgb(0, 0, 0)"),
      zaxis=dict(showgrid = False, title="z", range=[-100, 100], backgroundcolor="rgb(0, 0, 0)")
    )
  )

  data = [trace]
  plot_figure = go.Figure(data=data,  layout=layout)
  plot_figure.show()

def plot_bounding_box(data):

    point = data[:, 1]

    max_x = np.max(data[0], axis=0)
    max_y = np.max(data[1], axis=1)
    max_z = np.max(data[2], axis=2)

    min_y = np.min(data[0], axis=1)
    min_x = np.min(data[1], axis=0)
    min_z = np.min(data[2], axis=2)

    print(max_x, max_y, max_z, min_x, min_y, min_z)