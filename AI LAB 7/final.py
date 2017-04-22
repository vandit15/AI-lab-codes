# import statements
from anytree import NodeMixin, RenderTree, LevelGroupOrderIter
from copy import deepcopy

tree_list = [[] for iter in range(99)]
temp_list = [[] for iter in range(99)]

level = -1
string = ''
head_rules = {'S' : ['VP'], 'NP' : ['NN', 'NNS', 'NP'], 'VP' : ['VBD', 'VBZ', 'VP'], 'PP' : ['NN', 'NNS', 'NP'], 'ROOT' : [None]}

# Class for Tree Node
class MyNode(NodeMixin):
    def __init__(self, tag, head=None, parent=None):
        self.tag = tag
        self.head = head
        self.parent = parent

# Input from file and processing the input to get workable format
with open("inputnew.txt", "r") as input_file:
    for line in input_file:
        line = line.strip()
        #        print line
        string += " " + line
    string = string.replace(' ', '', 1)
    string = string.replace('(', '( ')
    string = string.replace(')', ' )')
    elem_list = string.split()
print elem_list
tags = []

# Getting the tags
for elem in elem_list:
    if elem_list[elem_list.index(elem) - 1] == '(':
        tags.append(elem)

tags = set(tags)
elem_list.remove('.')
elem_list.remove('.')
size = len(elem_list)

# Iterating over all the elements
for iter in range(size):
    # If opening parenthesis is encountered
    if elem_list[iter] == '(':
        level += 1
    # If a tag is encountered
    if elem_list[iter] in tags:
        temp_list[level].append(MyNode(elem_list[iter]))
        tree_list[level].append(MyNode(elem_list[iter]))
    # If a word is encountered
    if elem_list[iter] not in tags and elem_list[iter].isalpha():
        temp_list[level][-1].head = elem_list[iter]
        tree_list[level][-1].head = elem_list[iter]
    # If closing parenthesis encountered
    if elem_list[iter] == ')':
        level_size = len(temp_list[level])
        for index in range(level_size):
            if len(tree_list[level - 1]) > 0 and level >= 1:
                tree_list[level][-1].parent = tree_list[level - 1][-1]
        temp_list[level] = []
        level -= 1

# Function to get Dependency Tree from Phrase Structure Tree
def get_dep_tree(node, parent):
    if node.head == parent.head:
        temp = []
        for child in node.children:
            temp.append(child)
            child.parent = node.parent
        for elem in temp:
            get_dep_tree(elem, node.parent)
        node.parent = None
    else:
        for child in node.children:
            get_dep_tree(child, node)

ps_tree_list = deepcopy(tree_list)

# Function to determine heads of all levels in the Phrase Structure Tree
def find_heads(root_node):
    level_list = [[node for node in children] for children in LevelGroupOrderIter(root_node)]
    level_list_tags = [[(node.tag, node.head) for node in children] for children in LevelGroupOrderIter(root_node)]
    for iter in range(1,len(level_list) + 1):
        if iter == 1:
            pass
        for node in level_list[(-1)*iter]:
            if node.head:
                pass
            else:
                for elem in node.children:
                    if elem.tag in head_rules[node.tag]:
                        node.head = elem.head
                        break


find_heads(ps_tree_list[0][0])

# Print the Phrase Structure Tree
print "\nThe Phrase Structure Tree is:"
for pre, _, node in RenderTree(ps_tree_list[1][0]):
    treestr = u"%s%s (%s)" % (pre, node.tag, node.head)
    print treestr.ljust(10)
print

dep_tree_list = deepcopy(ps_tree_list)

get_dep_tree(dep_tree_list[1][0], dep_tree_list[0][0])

# Print the Dependency Tree
print "-"*99 + "\nThe Dependency Tree is:\n"
for pre, _, node in RenderTree(dep_tree_list[1][0]):
    treestr = u"%s%s" % (pre, node.head)
    print treestr.ljust(10)
print

# Set of karakas
karakas = {'k1' : [], 'k2' : [], 'k3' : [], 'k4' : [], 'k5' : [], 'k7' : []}

# Determining Karaka labels
for child in ps_tree_list[1][0].children:
    if child.tag == 'NP':
        karakas['k1'].append(child.head)
    if child.tag == 'VP':
        for child2 in child.children:
            if child2.tag == 'NP':
                karakas['k2'].append(child2.head)
            if child2.tag == 'PP':
                for child3 in child2.children:
                    if child3.tag == 'TO' and child3.head == 'to':
                        karakas['k4'].append(child2.head)
                    if child3.tag in ['IN', 'AT']:
                        if child3.head in ['in', 'at', 'over', 'on']:
                            print child3.tag
                            karakas['k7'].append(child2.head)
                        if child3.head == 'from':
                            print child3.tag
                            karakas['k5'].append(child2.head)
                        if child3.head == 'with':
                            print child3.tag
                            karakas['k3'].append(child2.head)

# Print Karaka labels
print "-"*99 + "\nKaraka labels are:\n"
for key in karakas:
    if len(karakas[key]) != 0:
        values = str(karakas[key]).replace("['", '')
        values = values.replace("']", '')
        print key + ": ", values
