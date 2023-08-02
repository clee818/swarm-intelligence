import main as main
import numpy as np
from matplotlib import pyplot as plt
import pylab
import seaborn


def get_files(filename_tail):
    locations = np.load(
        'data/location' + filename_tail + '.npy')  # np.load: returns arrays stored in this file
    adjacency_mat = np.load('data/adjacency_mat' + filename_tail + '.npy')
    return locations, adjacency_mat


def run_simulation(locations, adjacency_mat):
    colony = main.AntColony(locations, adjacency_mat, 0, locations.shape[0] - 1,
                            timesteps=1000, decay=0.1, n_ants=100)
    colony.run()
    print(colony.best_path)
    print(colony.best_path_dist)

    return colony


def plot(colony):
    plt.plot(colony.locations[:, 0][colony.best_path],
             colony.locations[:, 1][colony.best_path])
    plt.scatter(colony.locations[:, 0][colony.best_path],
                colony.locations[:, 1][colony.best_path])

    pylab.title("THE Best Path")
    plt.show()


def plot_pheromones(colony):
    p = np.copy(colony.pheromones)
    p[0][0] = 0
    p_norm = (p-np.min(p))/(np.max(p)-np.min(p))
    seaborn.heatmap(p_norm)
    plt.show()

"""
filename_tail = '10x10_maze1'
locations, adj_mat = get_files(filename_tail)
colony = run_simulation(locations, adj_mat)
plot_pheromones(colony)

"""