import pandas as pd
import numpy as np
from graphviz import Graph
from Tree import Node, Leaf, Edge, set_i, set_color


def export_dot(tree, filename):
    set_i()

    u = Graph('G', filename=filename, format='png')
    u.graph_attr.update(outputorder='edgesfirst', smoothing='triangle',
                         colorscheme='rdylgn10')

    u.edge_attr.update(arrowhead='vee', arrowsize='2', tailclip='false',
                       headclip='false', colorscheme='rdylgn10')

    u.node_attr.update(style='filled, rounded', outputorder='edgesfirst',
                       smoothing='triangle', colorscheme='rdylgn10')
    tree.print_dot(u, tree.nbr_samples)
    u.render()


def visualize_patient(input_data, tree, tree_nbr):
    set_color(tree_nbr)
    pat_nbr = 1
    patient = input_data.iloc[pat_nbr]
    target = -1
    done = False
    while not done:
        set_i()

        u = Graph('G', filename='trees/patients/{}/tree_{}/patient_depth_{'
                                '}'.format(
            pat_nbr, tree_nbr, target + 1), format='png')
        u.graph_attr.update(outputorder='edgesfirst', smoothing='triangle',
                             colors='whitesmoke', fontcolor='gray')

        u.edge_attr.update(arrowhead='vee', arrowsize='2', tailclip='false',
                           headclip='false', color='whitesmoke',
                           fontcolor='gray')

        u.node_attr.update(style='filled, rounded', outputorder='edgesfirst',
                           smoothing='triangle', color='whitesmoke',
                           fontcolor='gray')
        done = tree.visiulize_base(u, patient, 0, target)
        u.render()
        target += 1
        if done:
            ll = tree.left.find_leaf(tree.name, patient, 0, target)
            lr = tree.right.find_leaf(tree.name, patient, 0, target)
            u = Graph('G', filename='trees/patients/{}/tree_{}/patient_depth_{'
                                    '}'.format(
                pat_nbr, tree_nbr, target + 1), format='png')
            u.graph_attr.update(outputorder='edgesfirst', smoothing='triangle',
                                colors='whitesmoke', fontcolor='gray')

            u.edge_attr.update(arrowhead='vee', arrowsize='2', tailclip='false',
                               headclip='false', color='whitesmoke',
                               fontcolor='gray')

            u.node_attr.update(style='filled, rounded',
                               outputorder='edgesfirst',
                               smoothing='triangle', color='whitesmoke',
                               fontcolor='gray')
            if ll is not None:
                leaf = ll
            else:
                leaf = lr


            label = (
            str(int(np.round(leaf.good / leaf.nbr_samples, 2) * 100)) +
                "%")
            u.node(str(i), label=label, fillcolor='{},{},{}'.format(120*(leaf.good/leaf.nbr_samples)/360,1,1),
                     color = '{},{},{}'.format(120*(leaf.good/leaf.nbr_samples)/360,1,1), fontcolor='black',width='7', height='5', fontsize='20')
            u.render()
            print(target)
            return


    # u.view()
    #
    # u.body[0] = u.body[0].replace(']', ' fillcolor=blue]')
    # u.view()
    # for i in range(1, len(u.body)):
    #     item = u.body[i]
    #     print()


def add_last_im():
    pat_nr = 1
    u = Graph('G', filename='trees/patients/{}/final/final_im'.format(pat_nr), format='png')

    u.graph_attr.update(outputorder='edgesfirst', smoothing='triangle',
                     colors='whitesmoke', fontcolor='gray')

    u.edge_attr.update(arrowhead='vee', arrowsize='2', tailclip='false',
                     headclip='false', color='whitesmoke',
                     fontcolor='gray')

    u.node_attr.update(style='filled, rounded',
                     outputorder='edgesfirst',
                     smoothing='triangle', color='whitesmoke',
                    fontcolor='gray')
    filename = 'trees/patients/Probabilities/Probs_pat_{}.txt'.format(pat_nr+1)
    data = pd.read_csv(filename,sep=",",header = None)

    label = (
            str(int((data.iloc[0,0]) * 100)) +
                "%")

    u.node(str(0), label=label, fillcolor='{},{},{}'.format(120*data.iloc[0,0]/360,1,1),
                     color = '{},{},{}'.format(120*data.iloc[0,0]/360,1,1), fontcolor='black',width='7', height='5', fontsize='20')
    u.render()

def populate_tree(input_data, tree):
    for j in range(0, len(input_data)):
        row = input_data.iloc[j]
        tree.add_data(row)


def make_tree(filename):
    fid = open(filename + ".txt", 'r')
    node = Node('0', None)
    node.add_left(Edge(None, None))
    t = {}
    stack = [node]
    return build_tree(fid, stack, t)


def build_tree(fid, stack, tree):
    if stack == [] and tree:
        return tree
    last = stack[-1]
    if not last.left.is_connected() or (last.right is None or not
                                        last.right.is_connected()):

        line = fid.readline().replace('"', '').replace('\n', '').replace(' \\n', '')
        if len(line) < 2:
            return tree
        if ';' in line:
            [first, second] = line.lstrip(' ').split(';')
            [id_, name_, comp, cond] = first.split(' ')
            [criterion, statistic] = second.split(',')
            criterion = criterion.replace(' criterion = ', '')
            statistic = statistic.replace(' statistic = ', '')
            id_ = id_.rstrip(')')
            node = Node(id_, name_, criterion, statistic)

            if not last.left.is_connected():
                last.left.add_node(node)
            else:
                last.right.add_node(node)

            tree[id_] = node
            edge = Edge(cond, comp == '<=')

            if 'Sex' in name_:
                edge.sex = True

            node.add_left(edge)
            stack.append(node)

            return build_tree(fid, stack, tree)

        # Right branch
        elif '*' not in line:
            [id_, name_, comp, cond] = line.lstrip(' ').replace('\n',
                                                                '').split(' ')
            id_ = id_.rstrip(')')
            if id_ not in tree:
                tree[id_] = Node(id_, name_)
            node = tree[id_]
            edge = Edge(cond, comp == '<=')

            if 'Sex' in name_:
                edge.sex = True

            node.add_right(edge)
            return build_tree(fid, stack, tree)

        # leaf
        elif '*' in line:
            [id_, second] = line.lstrip(' ').split('*')
            a = second.replace('\n', '').rstrip(' ').split(' ')
            id_ = id_.rstrip(')')
            weight = a[len(a) - 1]
            leaf = Leaf(id_, weight)
            tree[id_] = leaf
            if not last.left.is_connected():
                edge = last.left
            else:
                edge = last.right
            edge.add_leaf(leaf)
            return build_tree(fid, stack, tree)
    else:
        stack.pop(-1)
        return build_tree(fid, stack, tree)


if __name__ == '__main__':
    for i in range(1, 401):
        name = 'trees/TreeTxt_{}'.format(i)
        root = make_tree(name)
        data = pd.read_excel("Imputed_Data.xlsx")
        populate_tree(data, root['1'])
        #export_dot(root['1'], name)
        visualize_patient(data, root['1'], i)

    add_last_im()