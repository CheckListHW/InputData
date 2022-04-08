import matplotlib.pyplot as plt
import numpy as np

from mvc.Model.map import Map, ExportRoof
from mvc.Model.point import Point
from utils.geometry.angle_line import intersection_segment_dot

if __name__ == '__main__':
    map = Map()
    map.load_from_json('C:/Users/KosachevIV/PycharmProjects/InputData/base.json')
    ExportRoof(map)

    a, b = [1, 2], [3,4]

    print([(a1, b1) for a1 in a for b1 in b])
