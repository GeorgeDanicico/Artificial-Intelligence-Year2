import math


class Point:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.cluster = None

    def distance(self, other_x, other_y):
        return math.dist((self.x, self.y), (other_x, other_y))

    def closest_cluster(self, clusters):
        return min(clusters, key=lambda centroid: self.distance(centroid.get_mean_x(), centroid.get_mean_y()))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, new_x):
        self.x = new_x

    def set_y(self, new_y):
        self.y = new_y

    def get_label(self):
        return self.label

    def set_label(self,  new_label):
        self.label = new_label
