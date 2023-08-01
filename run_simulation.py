import main as main
import numpy as np
from matplotlib import pyplot as plt
import pylab

locations = np.load('data/location10x10.npy') #np.load: returns arrays stored in this file
adjacency_mat = np.load('data/adjacency_mat10x10.npy')
colony = main.AntColony(locations, adjacency_mat, 0, 99, timesteps=100, decay=0.1)
colony.run()
print(colony.best_path)
print(colony.best_path_dist)

# pylab.title("Best Path ($n = " + str(n) + "$ steps)")
# plt.plot(colony.locations[colony.best_path])
# pylab.savefig("ant_colony_best_path"+str(n)+".png",bbox_inches="tight",dpi=600)
# pylab.show()

for i in range(len(colony.best_path)):
    plt.scatter(colony.locations[colony.best_path[i]][0],colony.locations[colony.best_path[i]][1])
pylab.title("THE Best Path")
plt.show()