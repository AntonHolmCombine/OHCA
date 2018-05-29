import numpy as np
global i


def set_i():
    global i
    i = 0


def set_color(j):
    global color
    color = 'mediumpurple1'


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
        self.good = 0

        self.graphviz_node = None

    def add_data(self, row):
        self.nbr_samples += 1
        good = self.left.add_data(row, self.name)
        good += self.right.add_data(row, self.name)
        self.good += good
        return good

    def add_left(self, node):
        self.left = node

    def add_right(self, node):
        self.right = node

    def print(self):
        print(self.id, self.name, 'nsamples =',  self.nbr_samples)

        self.left.print()
        self.right.print()

    def visiulize_base(self, u, patient, depth, target):
        global i, color
        a = str(i)

        name = nice_name(self.name)
        if depth <= target:

            u.node(str(i), label=name, fillcolor='{},{},{}'.format(120*(self.good/self.nbr_samples)/360,1,1),
                    color = '{},{},{}'.format(120*(self.good/self.nbr_samples)/360,1,1),
                   fontcolor='black')
        else:
            u.node(str(i), label=name)
        i += 1
        done = self.left.visiulize_base(u, a, self.name, patient, depth + 1,
                                        target)

        i += 1
        also_done = self.right.visiulize_base(u, a, self.name, patient,
                                             depth + 1,
                                         target)

        return done or also_done

    def print_dot(self, u, samples):
        global i
        a = str(i)

        name = self.nice_name(self.name)

        goodness = str(int(round(self.good/self.nbr_samples, 1)*100/11+1))
        u.node(str(i), label=name + "\n", fillcolor=goodness, color=goodness)

        i += 1
        self.left.print_dot(u, a, samples)
        i += 1
        self.right.print_dot(u, a, samples)


def nice_name( name):
    name = (name.replace('_', ' ').replace('P ', '').replace('B ', '').
            replace('A ', ''))
    return name


class Edge:
    def __init__(self, condition, less_than):
        self.condition = condition
        self.less_than = less_than
        self.node = None
        self.leaf = None
        self.connected = False
        self.good = 0
        self.nbr_samples = 0
        self.binary = False
        self.sex = False

        if condition == "0":
            self.binary = True

    def add_data(self, row, name):
        curr = row[name]
        if self.binary and (curr!= 1 and curr !=0):
            self.binary = False

        if (curr <= float(self.condition) and self.less_than) or (curr > float(
                self.condition) and not self.less_than):
            self.nbr_samples += 1
            if self.node:
                good = self.node.add_data(row)
            else:
                good = self.leaf.add_data(row)
            self.good += good
            return good
        return 0

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
        print(comp, self.condition, "nsamples = ", self.nbr_samples)
        if self.node:
            self.node.print()
        elif self.leaf:
            self.leaf.print()
        else:
            print("Something wrong")

    def visiulize_base(self, u, a, name, patient, depth, target):
        global color
        curr = patient[name]
        if self.less_than:
            if self.sex:
               b = 'Male'
            else:
               comp = '<='
               b = "No"

        else:
            if self.sex:
                b = 'Female'
            else:
                comp = '>'
                b = "Yes"

        if not self.binary:
            label = " " + comp + " " + str(
               self.condition) + " "
        else:
            label = b

        if (depth <= target and ((curr <= float(self.condition) and
            self.less_than) or (curr > float(self.condition) and
                                not self.less_than))):


            u.edge(a, str(i), label=label, splines='polyline',
                    tailclip='false', headclip='false',
                    fillcolor='{},{},{}'.format(120*(self.good/self.nbr_samples)/360,1,1), 
                    color='{},{},{}'.format(120*(self.good/self.nbr_samples)/360,1,1),
                    fontcolor='black')

        else:
            u.edge(a, str(i), label=label, splines='polyline',
                   tailclip='false', headclip='false')
            target = -1
        if self.node:
            done = self.node.visiulize_base(u, patient, depth+1, target)
        elif self.leaf:
            done = self.leaf.visiulize_base(u, patient, depth+1, target)

        else:
            print("Something wrong")
        return done

    def find_leaf(self, name, patient, depth, target):
        curr = patient[name]

        if (depth <= target and ((curr <= float(self.condition) and
            self.less_than) or (curr > float(self.condition) and
                                not self.less_than))):

            if self.node:
                ll = self.node.left.find_leaf(self.node.name, patient, depth +
                                                1, target)
                if ll is not None:
                    return ll
                lr = self.node.right.find_leaf(self.node.name, patient,
                                                 depth + 1, target)
                if lr is not None:
                    return lr
            elif self.leaf:
                return self.leaf



    def print_dot(self, u, a, samples):
        if self.less_than:
            if self.sex:
                b = 'Male'
            else:
                comp = '<='
                b = "No"
        else:
            if self.sex:
                b = 'Female'
            else:
                comp = '>'
                b = "Yes"

        if self.node:
            traffic = self.node.nbr_samples
        else:
            traffic = self.leaf.nbr_samples

        if not self.binary:
            label = " " + comp + " " + str(
                self.condition) + " "
        else:
            label = b
        penwidth = str(np.sqrt(traffic/samples)*50)
        node_traffic = round(np.sqrt(traffic / samples), 2)
        if self.nbr_samples >0:
            goodness = str(int(round(self.good/self.nbr_samples, 1)*100/11+1))
        else:
            print("Something wr")
            goodness = 5
        u.edge(a, str(i), label=label, splines='polyline', penwidth=penwidth,
               tailclip='false', headclip='false', color=goodness,
               fillcolor=goodness)

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
            return 1
        else:
            self.bad += 1
            return 0

    def print(self):
        print(self.id, self.weight, 'nsamples = ', self.nbr_samples)

    def print_dot(self, u, samples):
        goodness = str(int(round(self.good/self.nbr_samples, 1) * 100 / 11 + 1))

        if self.good >= self.bad:
            label = (str(int(np.round(self.good/self.nbr_samples, 2)*100)) +
                     "% of " + str(self.nbr_samples))
            u.node(str(i), label=label, fillcolor=goodness, color=goodness, )
        else:
            label = (str(int(np.round(self.good / self.nbr_samples, 2)*100)) +
                     "% of " + str(self.nbr_samples))
            u.node(str(i), label=label, color=goodness, fillcolor=goodness )

    def visiulize_base(self, u, patient, depth, target):
        if depth <= target:
            label = (str(int(np.round(self.good / self.nbr_samples, 2) * 100)) +
                "% ")
            u.node(str(i), label=label, fillcolor='{},{},{}'.format(120*(self.good/self.nbr_samples)/360,1,1),
                    color='{},{},{}'.format(120*(self.good/self.nbr_samples)/360,1,1), fontcolor='black')

            return True
        else:
            u.node(str(i), label="    ")
            return False



