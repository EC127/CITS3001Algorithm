import game
import copy


def blue_best_act(blue_t, green, energy_level):    # green for green_data, blue_t for blue action table
    best_evaluate_point = 0          # evaluation point for the best action
    best_incr = 0                    # number of voters added for the best action
    best_actnum = ''
    for act in blue_t.keys():       # for every action number
        if blue_t[act]['energy_lost'] > energy_level:      # not enough energy for this action
            continue
        test_data = copy.deepcopy(green)  # create the test data for stimulation for each action, reset for every iteration
        before_voter = count_voter(test_data)       # count how many voters are there
        game.blue_interact(test_data, blue_t, act)     # see the outcome of this action
        after_voter = count_voter(test_data)          # count how many voters after action
        incr_voter = after_voter - before_voter      # number of voters increase
        evaluate_point = incr_voter / blue_t[act]['energy_lost']    # how many voters increased per energy, aka action
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
    return best_actnum, best_incr                       # return the best action, and best increased number


def count_voter(data):
    # print('d', data)
    for keys in data.keys():
        voter_num = 0
        if data[keys]['opinion'] == 1:     # voter
            voter_num = voter_num + 1
    return voter_num


def grey_evaluate(blue_t, green, grey):    # grey represents grey_agents list
    num_blue = 0          # initialize the number of blue spy
    for spy in range(len(grey)):
        if grey[spy] == 1:    # blue spy
            num_blue = num_blue + 1

    proba_blue = num_blue / len(grey)      # the probability of getting a blue spy

    test_data = copy.deepcopy(green)  # create the test data for stimulation
    before_voter = count_voter(test_data)  # count how many voters are there
    game.blue_interact(test_data, blue_t, '10')  # see the outcome of the strongest action since it won't cost anything
    after_voter = count_voter(test_data)  # count how many voters after action
    incr_voter = after_voter - before_voter  # number of voters increase

    eva_grey = proba_blue * incr_voter - (1 - proba_blue) * incr_voter # assume the worst case, expectation

    return eva_grey


def blue_agent(blue_t, green, grey, energy_level):
    if len(grey) != 0:            # grey agent existed
        expect_incr = grey_evaluate(blue_t, green, grey)
        best_act, best_incr_num = blue_best_act(blue_t, green, energy_level)
        if best_incr_num > expect_incr:              # actions is better than activate a grey agent
            return best_act
        else:                                    # activate a grey agent is better
            return 'activate'
    else:
        best_act2, best_incr_num2 = blue_best_act(blue_t, green, energy_level)
        return best_act2
