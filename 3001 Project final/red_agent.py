import game
import copy


def red_best_act(red_t, green, follower_list):    # green for green_data, blue_t for blue action table
    best_evaluate_point = 0          # evaluation point for the best action
    best_incr = 0                    # number of voters added for the best action
    best_actnum = ''
    for act in red_t.keys():       # for every action number
        if red_t[act]['follower_lost'] > len(follower_list):      # not enough follower for this action
            continue
        test_data = copy.deepcopy(green)  # create the test data for stimulation for each action, reset for every iteration
        before_voter = count_voter(test_data)       # count how many voters are there
        game.red_interact(test_data, red_t, act, follower_list)     # see the outcome of this action
        after_voter = count_voter(test_data)          # count how many voters after action
        incr_voter = after_voter - before_voter      # number of voters increase
        evaluate_point = incr_voter / red_t[act]['follower_lost']    # how many voters increased per energy, aka action
        print(evaluate_point)
        # efficiency
        if evaluate_point > best_evaluate_point:        # if this action is better
            best_evaluate_point = evaluate_point       # update best eva point and best action number and best incr num
            best_actnum = act
            best_incr = incr_voter
        elif evaluate_point == best_evaluate_point:    # if eva point is the same , compare the increased number
            if incr_voter >= best_incr:
                best_actnum = act                  # update  best action number, best incr num
                best_incr = incr_voter
    # print(green)
    return best_actnum                       # return the best action


def count_voter(data):
    # print('d', data)
    for keys in data.keys():
        voter_num = 0
        if data[keys]['opinion'] == 0:     # non-voter
            voter_num = voter_num + 1
    return voter_num


def red_agent(red_t, green, follower_list):
    best_act = red_best_act(red_t, green, follower_list)
    return best_act