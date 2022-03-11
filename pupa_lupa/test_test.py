import numpy as np
from matplotlib import pyplot as plt

from Tools.filedialog import dict_from_json


class Body:

    def __init__(self, name):
        self.name = name
        self.columns = {}

    def add_dot(self, x, y, z):
        if self.columns.get('{0}_{1}'.format(x, y)):
            self.columns['{0}_{1}'.format(x, y)].append(z)
        else:
            self.columns['{0}_{1}'.format(x, y)] = [z]


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    data_voxel = np.zeros([25, 25, 51], dtype=bool)
    data: dict = dict_from_json('C:/Users/KosachevIV/PycharmProjects/InputData/lay_name133.json')

    bodys = {}
    for body_name in data:
        bodys[body_name] = Body(body_name)
        for x in data[body_name]:
            for y in data[body_name][x]:
                for s_e in data[body_name][x][y]:
                    for z in range(s_e['s'], s_e['e']+1):
                        bodys[body_name].add_dot(x, y, z)
                        data_voxel[int(x)][int(y)][int(z)] = True
        ax.voxels(data_voxel)

    plt.show()

