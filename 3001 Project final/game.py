import easygui as ui
import random


def g_interact(node1, node2, green_data):
    # if they have different opinion
    if green_data[node1]['opinion'] != green_data[node2]['opinion']:
        # if node1 is more certain
        if green_data[node1]['uncertainty'] < green_data[node2]['uncertainty']:
            # then node2 changes its opinion
            green_data[node2]['opinion'] = green_data[node1]['opinion']
            green_data[node2]['uncertainty'] = 10 - \
                green_data[node2]['uncertainty'] + \
                green_data[node1]['uncertainty']
            # more certain the origin opinion is, more uncertain the changed opinion will be
        # if node2 is more certain
        elif green_data[node1]['uncertainty'] > green_data[node1]['uncertainty']:
            # then node1 changes its opinion
            green_data[node1]['opinion'] = green_data[node2]['opinion']
            green_data[node1]['uncertainty'] = 10 - \
                green_data[node1]['uncertainty'] + \
                green_data[node2]['uncertainty']
            # more certain the origin opinion is, more uncertain the changed opinion will be

# only node1 can be red or blue


def r_interact(node2, green_data, red_actable, act):
    if green_data[node2]['opinion'] == 0:     # the green node chooses not to vote
        green_data[node2]['uncertainty'] = round(
            green_data[node2]['uncertainty']/2)   # node 2 is more certain
    else:                                     # the green node chooses to vote
        if red_actable[act]['uncertainty'] < green_data[node2]['uncertainty']:
            # then node2 changes its opinion
            green_data[node2]['opinion'] = 0
            green_data[node2]['uncertainty'] = 10 - \
                green_data[node2]['uncertainty'] + \
                red_actable[act]['uncertainty']
            # more certain the origin opinion is, more uncertain the changed opinion will be
        else:                          # node2 is certain about it's opinion
            # node2 now is more uncertain
            green_data[node2]['uncertainty'] = red_actable[act]['uncertainty']


def b_interact(node2, green_data, blue_actable, act):
    if green_data[node2]['opinion'] == 1:     # the green node chooses to vote
        green_data[node2]['uncertainty'] = round(
            green_data[node2]['uncertainty']/2)   # node 2 is more certain
    else:                                     # the green node chooses not to vote
        if blue_actable[act]['uncertainty'] < green_data[node2]['uncertainty']:
            # then node2 changes its opinion
            green_data[node2]['opinion'] = 1
            green_data[node2]['uncertainty'] = 10 - \
                green_data[node2]['uncertainty'] + \
                blue_actable[act]['uncertainty']
            # more certain the origin opinion is, more uncertain the changed opinion will be
        else:                          # node2 is certain about it's opinion
            # node2 now is more uncertain
            green_data[node2]['uncertainty'] = blue_actable[act]['uncertainty']


def green_interact(green_data, graph):
    incident_spread_probability = round(random.randint(
        1, 99) * 0.01, 2)   # the probability of spreading
    print(green_data)
    print(incident_spread_probability)
    for key in graph.adjacency_list.keys():
        # print(key)
        # turn set into list for visit
        g_list = list(graph.adjacency_list[key])
        # print(g_list)
        if g_list:
            for edge in g_list:
                if edge[1] >= incident_spread_probability:    # the interaction can happen
                    g_interact(key, edge[0], green_data)
                    # print((key, edge[0]))
    print(green_data)


def blue_interact(green_data, blue_actable, act):
    for node in green_data.keys():
        b_interact(node, green_data, blue_actable, act)


def red_interact(green_data, red_actable, act, follower_list):
    for node in follower_list:
        r_interact(node, green_data, red_actable, act)