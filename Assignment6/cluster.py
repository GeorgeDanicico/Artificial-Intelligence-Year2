import operator


class Cluster:
    def __init__(self, label):
        self.label = label
        self.points = []
        self.mean_x = 0
        self.mean_y = 0
        self.curr_iter = 0
        self.max_iter = 1500

    def get_label(self):
        return self.label

    def get_mean_x(self):
        return self.mean_x

    def set_mean_x(self, new_mean_x):
        self.mean_x = new_mean_x

    def get_mean_y(self):
        return self.mean_y

    def set_mean_y(self, new_mean_y):
        self.mean_y = new_mean_y

    def add_point(self, point):
        # add the point to this cluster
        self.points.append(point)

        # check if the point belongs to other cluster and delete it from the other cluster
        if point.cluster:
            point.cluster.points.remove(point)

        point.cluster = self
        return self.update_centroid()

    def update_centroid(self):
        # update the centroid of the cluster
        old_centroid_x = self.mean_x
        old_centroid_y = self.mean_y

        x_mean = 0
        y_mean = 0

        for point in self.points:
            x_mean += point.get_x()
            y_mean += point.get_y()

        self.mean_x = x_mean / len(self.points)
        self.mean_y = y_mean / len(self.points)
        self.curr_iter += 1

        if self.curr_iter >= self.max_iter:
            return False
        # if there is no big difference when changing the centroid
        if abs(self.mean_x - old_centroid_x) <= 0.000001 and abs(self.mean_y - old_centroid_y) <= 0.000001:
            return False
        return True

    def update_label(self):
        freq = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

        for point in self.points:
            freq[point.label] += 1

        max_frequency = freq['A']
        self.label = 'A'

        for fr in freq.keys():
            if freq[fr] > max_frequency:
                max_frequency = freq[fr]
                self.label = fr

    def compute_statistics(self, points):
        true_positive = false_positive = true_negative = false_negative = 0

        for point in self.points:
            if point.label == self.label:
                true_positive += 1
            else:
                false_positive += 1
        for point in points:
            if point not in self.points and point.cluster.label != self.label:
                if point.get_label() != self.label:
                    true_negative += 1
                else:
                    false_negative += 1

        accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_positive + false_negative)
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        score = 2 * precision * recall / (precision + recall)

        return accuracy, precision, recall, score
