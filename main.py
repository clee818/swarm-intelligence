# Swarm intelligence - Ant colony optimization
# import random as rn
import numpy as np


class AntColony():
    def __init__(self, locations, adjacency_mat, start, end, n_ants=100,
                 timesteps=1000, alpha=1, beta=2, decay=0.1):
        # initializing all variables that we will use
        self.locations = locations  # matrix of locations n rows by 2 col
        self.adjacency_mat = adjacency_mat
        self.pheromones = np.ones(
            adjacency_mat.shape)  # creating matrix of pheromones

        self.start = start  # starting location of ant
        self.end = end  # ending point of path ant follows
        self.n_ants = n_ants  # number of ants
        self.timesteps = timesteps  # a counter that controls when ants move and when pheromones decay
        self.alpha = alpha  # weight of pheromone
        self.beta = beta  # weight of distance
        self.decay = decay  # decay rate of pheromone

        self.best_path = []
        self.best_path_dist = np.inf

    def run(self):
        paths = []
        for i in range(self.n_ants):
            paths.append([self.start])  # building path array
        for t in range(1, self.timesteps):
            self.run_time_step(paths, t)
            self.p_decay()
        self.clean_best_path()

    def clean_best_path(self):
        for i in range(len(self.best_path)-1, -1, -1):
            if self.best_path[i] == self.start:
                self.best_path = self.best_path[i:]
                break



    def run_time_step(self, paths, t):
        for a in range(self.n_ants):
            next_pos = self.gen_step(paths[a][t-1], paths[a])
            paths[a].append(next_pos)
            if next_pos == -1:
                paths[a] = [self.start] * len(paths[a])
                continue
            if next_pos == self.end:
                self.p_add(paths[a])
                dist = self.get_path_distance(paths[a])
                if (dist < self.best_path_dist):
                    self.best_path = paths[a]
                    self.best_path_dist = dist
                paths[a] = [self.start]*len(paths[a])


    def gen_step(self, position, path):
        # return -1 if no moves left
        # return index of next position in location matrix

        possible_steps = np.copy(self.adjacency_mat[position])
        possible_steps[path[:-1]] = 0

        if np.sum(possible_steps) == 0:  # if no moves left
            return -1

        possible_steps[possible_steps == 0] = np.inf

        probs = (self.pheromones[position] ** self.alpha) * (
                    (1.0 / possible_steps) ** self.beta)

        norm_probs = probs / probs.sum()

        new_position = np.random.choice(np.arange(len(self.locations)), 1,
                                        p=norm_probs)
        return int(new_position)

    def p_add(self, path):
        for r in range(len(path) - 1):
            self.pheromones[path[r], path[r + 1]] += 1.0
            self.pheromones[path[r + 1], path[
                r]] += 1.0  # update pheromones matrix row at every path int

    def get_path_distance(self, path):
        total_distance = 0
        for r in range(len(path) - 1):
            total_distance += self.adjacency_mat[path[r], path[r + 1]]
        return total_distance

    def p_decay(self):
        # P(1/D)
        # keeps track of pheromone strength and decay rate
        self.pheromones = self.pheromones * (1.0 - self.decay)
        # 0 < decay < 1
