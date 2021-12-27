import matplotlib.pyplot as plt

if __name__ == '__main__':
    # pre
    s = 15

    x = [s*0.4, s*0.4, s*0.1, s*0.1, s*0.4, s*0.4, s*0.6, s*0.6, s*0.9, s*0.9, s*0.9, s*0.6, s*0.6]
    y = [s*0.1, s*0.4, s*0.4, s*0.6, s*0.6, s*0.9, s*0.9, s*0.6, s*0.6, s*0.4, s*0.4, s*0.4, s*0.1]
    plt.plot(x, y, color='black')


    plt.show()
