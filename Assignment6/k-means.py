from random import sample

from cluster import Cluster
from statistics import *

if __name__ == '__main__':
    clusters = [Cluster('A'), Cluster('B'), Cluster('C'), Cluster('D')]
    points = read_points_from_file()
    random_points = sample(points, 4)

    for i in range(4):
        clusters[i].mean_x = random_points[i].x
        clusters[i].mean_y = random_points[i].y

    ok = True
    while ok:
        ok = False
        for p in points:
            optimal_cluster = p.closest_cluster(clusters)
            if optimal_cluster.add_point(p):
                ok = True

    for cluster in clusters:
        cluster.update_label()
    show_statistics(clusters, points)
    plot(clusters)
