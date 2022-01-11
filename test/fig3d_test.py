from Controllers.Editor.draw3d import *
from matplotlib import pyplot as plt
from Model.figure_3d import Figure3d


if __name__ == '__main__':
    fig3d = Figure3d(path='C:/Users/KosachevIV/PycharmProjects/InputData/layers/lay_name173.json')
    Draw = DrawVoxels(fig3d=fig3d)

