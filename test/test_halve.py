from random import random

import matplotlib.pyplot as plt

from archive.dot_count_change import halve_dot_count

if __name__ == '__main__':
    x = [float(i) for i in range(100)] + [random() / 2 + 100 for _ in range(100)] + \
        [i for i in reversed(range(100))] + [random() / 2 for i in range(100)]

    y = [random() / 2 for _ in range(100)] + [i for i in range(100)] + \
        [random() / 2 + 100 for _ in range(100)] + [i for i in reversed(range(100))]

    plt.plot(x, y)

    x, y = halve_dot_count(x, y)
    plt.plot(x, y)
    plt.show()
