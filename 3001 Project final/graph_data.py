import random


class Graph:            # this Graph is design for this project, refer to undirected graph
    def __init__(self, num_of_nodes):
        self.num_of_nodes = num_of_nodes
        self.adjacency_list = {node: set() for node in range(num_of_nodes)}

    # weight here represent the probability of interaction
    def add_edge(self, node1, node2, weight):
        self.adjacency_list[node1].add((node2, weight))
        # self.adjacency_list[node2].add((node1, weight))  one edge means both ways

    def print_adj_list(self):
        for key in self.adjacency_list.keys():
            print(f'node {key} : {self.adjacency_list[key]}')


def create_graph(number_of_nodes, probability, graph):
    # size_of_all_edge = (number_of_nodes * (number_of_nodes - 1)) / 2
    all_edge = []    # create an empty list to store all possible edges
    counter = 0      # store the number of possible edges
    for i in range(number_of_nodes-1):
        for k in range(i+1, number_of_nodes):
            # print(i, k)
            all_edge.append([i, k])    # store every possible edges
            counter = counter + 1      # get the number of possible edges
    # print(all_edge)
    # print(counter)
    # get the number of exist edges
    number_of_edges = round(counter * probability)
    # print(number_of_edges)
    node_list = []                     # to get rid of the repeated number
    for m in range(number_of_edges):
        # randomly pick an edge to be place in the graph
        rn = random.randint(0, counter - 1)
        # print(rn)
        while rn in node_list:
            # remake another random number
            rn = random.randint(0, counter - 1)
        node_list.append(rn)
        # randomly pick probability of interaction as weight
        rw = round(random.randint(1, 99) * 0.01, 2)
        # add the random edge to graph
        graph.add_edge(all_edge[rn][0], all_edge[rn][1], rw)


def create_database(starting_uncertainty, percentage_of_voter, number_of_nodes, greendb):
    # the number of voters
    voter_number = round(percentage_of_voter * number_of_nodes)
    voter_list = []                            # the list of nodes which decide to vote
    for x in range(voter_number):
        # the random chosen node
        r_node = random.randint(0, number_of_nodes - 1)
        while r_node in voter_list:
            # when the random node already in the list, remake one
            r_node = random.randint(0, number_of_nodes - 1)
        # append the node in to voter_list
        voter_list.append(r_node)
        # print(voter_list)
    for y in range(number_of_nodes):
        if y in voter_list:
            # 1 for voter, 0 for non-voter
            greendb.setdefault(y, {})['opinion'] = 1
        else:
            greendb.setdefault(y, {})['opinion'] = 0
        # put the uncertainty in
        greendb.setdefault(y, {})['uncertainty'] = starting_uncertainty