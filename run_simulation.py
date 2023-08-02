import main as main
import numpy as np
from matplotlib import pyplot as plt
import pylab


def run_simulation(filename_tail, plot=True):
    locations = np.load(
        'data/location' + filename_tail + '.npy')  # np.load: returns arrays stored in this file
    adjacency_mat = np.load('data/adjacency_mat' + filename_tail + '.npy')
    colony = main.AntColony(locations, adjacency_mat, 0, locations.shape[0] - 1,
                            timesteps=1000, decay=0.1, n_ants=100)
    colony.run()
    print(colony.best_path)
    print(colony.best_path_dist)

    if plot:
        plt.plot(colony.locations[:, 0][colony.best_path],
                 colony.locations[:, 1][colony.best_path])
        plt.scatter(colony.locations[:, 0][colony.best_path],
                    colony.locations[:, 1][colony.best_path])

        pylab.title("THE Best Path")
        plt.show()


filename_tail = '10x10_maze1'
run_simulation(filename_tail, plot=True)
