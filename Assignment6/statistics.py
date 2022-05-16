import csv

import matplotlib.pyplot as plt

from point import Point


def read_points_from_file():
    points = []

    with open('dataset.csv') as file:
        reader = csv.reader(file, delimiter=',')

        for row in reader:
            # ignore the first line that represents the headers for each column
            if row[0] != 'label':
                point = Point(float(row[1]), float(row[2]), row[0])
                points.append(point)

    return points


def show_statistics(clusters, points):

    for cluster in clusters:
        accuracy, precision, recall, score = cluster.compute_statistics(points)

        print(cluster.label)
        print("Accuracy " + str(accuracy))
        print("Precision " + str(precision))
        print("Recall " + str(recall))
        print("F1-Score " + str(score))
        print("\n")


def plot(clusters):
    for cluster in clusters:

        x = [point.get_x() for point in cluster.points]
        y = [point.get_y() for point in cluster.points]
        symbol = ''

        if cluster.label == 'A':
            symbol = 'ro'
        if cluster.label == 'B':
            symbol = 'co'
        if cluster.label == 'C':
            symbol = 'go'
        if cluster.label == 'D':
            symbol = 'mo'

        plt.plot(x, y, symbol, label=cluster.get_label())
        plt.plot(cluster.get_mean_x(), cluster.get_mean_y(), 'kx')

    plt.legend()
    plt.show()
