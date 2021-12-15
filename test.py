def decomposition(n):
    return [bit == "1" for bit in reversed(format(n, "b"))]

def completion(list_bits, n):
    length = len(list_bits)
    if n > length:
        return list_bits + [False] * (n - length)
    else:
        return list_bits[:n]

def table(x, n):
    return completion(decomposition(x), n)

class Node:
    def __init__(self, label, left, right):
        self.label = label 
        self.left = left 
        self.right = right
        self.luka = "" 
    def get_left(self):
        return self.left
    def get_right(self):
        return self.right
    def set_left(self, left):
        self.left = left
    def set_right(self, right):
        self.right = right  
    def get_label(self):
        return self.label
    def set_label(self, label):
        self.label = label
    def set_luka(self, luka_word):
        self.luka = luka_word
    def get_luka(self):
        return self.luka
    def __str__(self):
        # if self.left is None and self.right is None:
        #     return str(self.label)
        # else:
        #     return str(self.label) +  " " + self.left.__str__() + " " + self.right.__str__()
        return str(self.label) +  " Left: (" + self.left.__str__() + ") Right: (" + self.right.__str__() + ")"

import math

def traverse_tree(tree, list_vars, truth_table, count):
    if count != len(list_vars) - 1:
        if tree is None:
            tree = Node(list_vars[count], None, None)
            
        left = traverse_tree(None, list_vars, truth_table, count+1)
        right = traverse_tree(None, list_vars, truth_table, count+1)
        tree.set_left(left)
        tree.set_right(right)
        return tree
    else:
        value1 = truth_table.pop(0)
        value2 = truth_table.pop(0)
        return Node(list_vars[count], Node(value1, None, None), Node(value2, None, None))

def cons_arbre(truth_table):
    nb_vars = math.log2(len(truth_table))
    if nb_vars - int(nb_vars) != 0:
        return None

    list_vars = [x for x in range(1, int(nb_vars)+1)]
    # random.shuffle(list_vars)
    return traverse_tree(None, list_vars, truth_table, 0)

def luka(tree):
    if tree.get_left() is None and tree.get_right() is None:
        new_luka_word = str(tree.get_label())
        tree.set_luka(new_luka_word)
    else:
        luka(tree.get_left())
        luka(tree.get_right())
        left = tree.get_left()
        right = tree.get_right()
        tree.set_luka(str(tree.get_label()) + "(" + left.get_luka() + ")" + "(" + right.get_luka() + ")")


def compression_bdd(luka_tree, seen):
    if luka_tree.get_left() is None and luka_tree.get_right() is None:
        luka_word = luka_tree.get_luka()
        if luka_word in seen:
            return seen[luka_word], 0
        else:
            seen[luka_word] = luka_tree
            return luka_tree, 1
    
    # Deletion rule
    left, right = luka_tree.get_left(), luka_tree.get_right()
    if left is not None and right is not None:
        left_luka_word, right_luka_word = left.get_luka(), right.get_luka()
        if left_luka_word == right_luka_word:
            if left_luka_word in seen:
                return seen[left_luka_word], 0
            else:
                # seen[left_luka_word] = left
                new_left, child_node_count = compression_bdd(left, seen)
                seen[luka_tree.get_luka()] = new_left
                return new_left, child_node_count

    # Termination rule and merging rule
    luka_word = luka_tree.get_luka()
    if luka_word in seen:
        return seen[luka_word], 0
    else:
        seen[luka_word] = luka_tree
        compact_tree = luka_tree
        # print(f"Luka word: {compact_tree.get_luka()}")
        # print(f"Id tree: {hex(id(compact_tree))}")
        new_left, left_child_node_count = compression_bdd(luka_tree.get_left(), seen)
        # print(f"Id left: {hex(id(new_left))}")
        compact_tree.set_left(new_left)
        # print(f"Id left tree: {hex(id(compact_tree.get_left()))}")
        new_right, right_child_node_count = compression_bdd(luka_tree.get_right(), seen)
        # print(f"Id right: {hex(id(new_right))}")
        compact_tree.set_right(new_right)
        # print(f"Id right tree: {hex(id(compact_tree.get_right()))}")

        return compact_tree, left_child_node_count + right_child_node_count + 1

import time
import matplotlib.pyplot as plt
from collections import defaultdict

def calculate_exact_distribution(n):
    nb_functions = defaultdict(lambda : 0)
    for i in range(2 ** (2 ** n)):
        tree = cons_arbre(table(i, 2 ** n))
        luka(tree)
        _, nb_nodes = compression_bdd(tree, dict())
        nb_functions[nb_nodes] += 1

    datas = sorted(list(zip(nb_functions.keys(), nb_functions.values())), key=lambda x: x[0])
    x = [data[0] for data in datas]
    y = [data[1] for data in datas]
    plt.plot(x, y, "bo-")
    plt.xlabel(f"ROBDD node count for {n} variables")
    plt.ylabel(f"Number of Boolean functions")
    plt.grid()
    plt.show()

calculate_exact_distribution(5)