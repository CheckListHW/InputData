from Controllers.Editor.draw_shape import *
from matplotlib import pyplot as plt
from Model.shape import Shape


if __name__ == '__main__':
    fig3d = Shape(path='C:/Users/KosachevIV/PycharmProjects/InputData/layers/lay_name173.json')
    Draw = DrawVoxels(fig3d=fig3d)

