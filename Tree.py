import numpy as np
global i


def set_i():
    global i
    i = 0


class Node:
    def __init__(self, id, name, criterion=None,
                 statistic=None):
        self.id = id
        self.name = name
        self.criterion = criterion
        self.statistic = statistic

        self.left = None
        self.right = None
        self.nbr_samples = 0

    def add_data(self, row):
        self.nbr_samples += 1
        self.left.add_data(row, self.name)
        self.right.add_data(row, self.name)

    def add_left(self, node):
        self.left = node

    def add_right(self, node):
        self.right = node

    def print(self):

        print(self.id, self.name, 'nsamples =',
              self.nbr_samples)
        if self.left:
            self.left.print()
        if self.right:
            self.right.print()

    def print_dot(self, u, samples):
        global i
        name = (self.name.replace('_', ' ').replace('P ', '').replace('B ', '').
                replace('A ', ''))
        traffic = round(np.sqrt(self.nbr_samples/samples), 2)
        u.node(str(i), label=name + "\n",
               fillcolor=(".55 " + str(traffic) + " 0.999"),
               color=(".55 " + str(traffic) + " 0.999"))
        a = str(i)

        if self.left:
            i += 1
            self.left.print_dot(u, a, samples)

        if self.right:
            i += 1
            self.right.print_dot(u, a, samples)


class Edge:
    def __init__(self, condition, less_than):
        self.condition = condition
        self.less_than = less_than
        self.node = None
        self.leaf = None
        self.connected = False

    def add_data(self, row, name):
        curr = row[name]

        if (curr <= float(self.condition) and self.less_than) or (curr > float(
                self.condition) and not self.less_than):
            if self.node:
                self.node.add_data(row)
            else:
                self.leaf.add_data(row)

    def is_connected(self):
        return self.connected

    def add_node(self, node):
        self.node = node
        self.connected = True

    def add_leaf(self, leaf):
        self.leaf = leaf
        self.connected = True

    def print(self):
        if self.less_than:
            comp = '<='
        else:
            comp = '>'
        print(comp, self.condition)
        if self.node:
            self.node.print()
        elif self.leaf:
            self.leaf.print()
        else:
            print("Something wrong")

    def print_dot(self, u, a, samples):
        if self.less_than:
            comp = '<='
        else:
            comp = '>'

        if self.node:
            traffic = self.node.nbr_samples
        else:
            traffic = self.leaf.nbr_samples

        penwidth = str(np.sqrt(traffic/samples)*50)
        node_traffic = round(np.sqrt(traffic / samples), 2)
        u.edge(a, str(i), label=" " + comp + " " + str(
            self.condition) + " ", splines='polyline', penwidth=penwidth,
               tailclip='false', headclip='false',
               color=(".55 " + str(node_traffic) + " 0.999"))

        if self.node:
            self.node.print_dot(u, samples)
        elif self.leaf:
            self.leaf.print_dot(u, samples)
        else:
            print("Something wrong")


class Leaf:
    def __init__(self, id, weight):
        self.id = id
        self.weight = weight
        self.nbr_samples = 0
        self.good = 0
        self.bad = 0

    def add_data(self, row):
        self.nbr_samples += 1
        if row['Binary_Sec_Out_180_day_CPC_score'] == 0:
            self.good += 1
        else:
            self.bad += 1

    def print(self):
        print(self.id, self.weight, 'nsamples = ', self.nbr_samples)

    def print_dot(self, u, samples):
        traffic = round(self.nbr_samples / samples, 2)

        if self.good >= self.bad:
            label = (str(int(np.round(self.good/self.nbr_samples, 2)*100)) +
                     "% of " + str(self.nbr_samples))
            color = (".4 " + str(np.round(self.good/self.nbr_samples, 2)
                                 * 1.2 - 0.5) + " 0.999")
            u.node(str(i), label=label,
                   fillcolor=color, color=color, )
        else:
            label = (str(int(np.round(self.good / self.nbr_samples, 2)*100)) +
                     "% of " + str(self.nbr_samples))
            color = (".01 " + str(np.round(self.bad / self.nbr_samples, 2)
                                  * 1.2 - 0.5) + " 0.999")
            u.node(str(i), label=label,  color=color, fillcolor=color )
