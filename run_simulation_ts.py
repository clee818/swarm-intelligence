import numpy as np
import matplotlib.pyplot as plt
from AntColonyTS import AntColony

distances = np.array([[np.inf, 2, 2, 5, 7],
                      [2, np.inf, 4, 8, 2],
                      [2, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])

colony = AntColony(distances, 1, 1, 100, 0.95, alpha=1, beta=1)
best_path = colony.run()
print("shortest_path: {}".format(best_path))



plt.title("THE Best Path")
plt.show()
