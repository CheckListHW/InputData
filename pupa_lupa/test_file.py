import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt


def func(x, y):
    return x + y


points = [[0, 0], [0, 25], [25, 25], [25, 0]]
val = [0, 0, 0, 0]
size = 25


points.append([5, 5])
val.append(1)

points = np.array(points)
val = np.array(val)


grid_x, grid_y = np.mgrid[0:size:25j, 0:size:25j]
grid_z = griddata(points, val, (grid_x, grid_y), method='cubic')

for zz, i1 in zip(grid_z, range(len(grid_z)+1)):
    for z, j in zip(zz, range(len(zz)+1)):
        if '{0}, {1}'.format(i1, j) in ['{0}, {1}'.format(i[0], i[1])for i in points]:
            print(i1, j, round(z * 1000) / 1000)

print([0, 2] in points)

plt.imshow(grid_z.T, extent=(0, 1, 0, 1), origin='lower')
# plt.scatter(points[:, 0], points[:, 1], c='k')

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_wireframe(grid_x, grid_y, grid_z)

plt.show()
