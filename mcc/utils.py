import numpy as np

def distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

def random_point(dimensions):
    return np.random.rand(dimensions)
