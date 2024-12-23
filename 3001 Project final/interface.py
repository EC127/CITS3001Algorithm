import easygui as ui
import sys
import actions as act
import game
import graph_data as gd
import helper
import random
import blue_agent as ba
import red_agent as ra


def print_status():
    massage = 'Overview: \nPeople who wants to vote: {}\nPeople who will not vote: {} \nAvailable spy: {} \n\nThe Red Party: \nCurrent follower lost is: {}\n\nBlue team: \nCurrent budget is: {}'.format(
        helper.get_vote_people(green_data), num_green - helper.get_vote_people(green_data), num_grey, follower_lost, energy_level)
    ui.msgbox(massage, 'State')


def game_over():
    ui.msgbox(msg='The Blue Party used up their budget and The Red Party has no follower\nGame Over',
                  title='The End', ok_button='Result')
    ui.msgbox(msg='Result: \n{} \n\nDetails: \nPeople who wants to vote: {}\nPeople who will not vote: {} \n\nBlue Team: \nUsed spy: {} times \n\nThe Red Party: \nFollower lost in the end is: {}\nRound {}'.format(helper.game_result(green_data), helper.get_vote_people(green_data), num_green - helper.get_vote_people(green_data), origin_grey - num_grey, follower_lost, round_counter),
              title='Game Result', ok_button='OK')
    # End the game
    sys.exit(0)


# start up
if ui.ccbox('Welcome to the Game!', 'The Red Party VS The Blue Party', choices=('Start', 'Exit')):
    ui.msgbox(msg='There is a country.\n\nWhere there\'s a Red Party that want to keep people from voting to promote their authoritarian government.\n\nMeanwhile there is a Blue Party trying to stop the Red Party and promote democratic government in the country.\n\nHowever, there are also some foreign forces hiding there, waiting for chances.\n\nNow, Election day is approaching...', title='Background')
# end if Exit is chosen
else:
    sys.exit(0)

'''
parameters
0: num_green: number of population
1: starting_uncertainty: People's uncertainty at the beginning of the game
2: probab_connect: Probability of connections between people
3: num_grey: number of spies
4: num_redspy = percent_redspy * num_grey: Number of red spy in the grey team
5: init_true: Percentage of population who want to vote
'''

# Intergerbox for entering parameters
num_green = ui.integerbox(
    "Population [100 <= value <= 1000]", "Please Set Your Start-up Parameters", lowerbound=100, upperbound=1000, default=100)

starting_uncertainty = ui.integerbox(
    "Starting uncertainty [0 <= value <= 10]", "Please Set Your Start-up Parameters", lowerbound=0, upperbound=10, default=9)

probab_connect = 0.1 * ui.integerbox(
    # probability would be 0 - 1, which is input*0.1
    "Probability of connections[0 < value < 10]",
    "Please Set Your Start-up Parameters", lowerbound=1, upperbound=9, default=5)

num_grey = ui.integerbox(
    "Total number of Spies [< Population]", "Please Set Your Start-up Parameters", lowerbound=1, upperbound=num_green, default=5)
origin_grey = num_grey  # for end game evaluate

num_redspy = ui.integerbox(
    "Number of Red Spies [< Total number of Spy]", "Please Set Your Start-up Parameters", lowerbound=0,
    upperbound=num_grey - 1, default=2)

init_true = 0.01 * ui.integerbox(
    # Percentage would be 0 - 1 (0 - 100%), which is input*0.01
    "Percentage of population who want to vote [0% to 100%]", "Please Set Your Start-up Parameters", lowerbound=0,
    upperbound=100, default=50)


# Game started, initialise the game
# The Red Party
follower_lost = 0
red_actable = {}

# Blue Team
energy_level = 50
blue_actable = {}

# Grey Team
grey_agents = []
for x in range(num_grey):
    if num_redspy != 0:
        grey_agents.append(0)  # red spy
        num_redspy = num_redspy - 1
    else:
        grey_agents.append(1)  # blue spy
print(grey_agents)
print(len(grey_agents))

# Initialise actable
act.create_actions(red_actable, blue_actable, num_green)

# Initialise follower list for red agent
follower_list = []
for x in range(num_green):
    follower_list.append(x)
# print(follower_list)

# Initialise graph
g = gd.Graph(num_green)
gd.create_graph(num_green, probab_connect, g)

# Initialise green node initial status
green_data = {}
gd.create_database(starting_uncertainty, init_true, num_green, green_data)

ui.msgbox(msg='Parameters are Set, Click Start to Continue',
          title='Parameters', ok_button='Start')
g.print_adj_list()

# Initialise round counter
round_counter = 0

# Initialise messages
red_choice_msg = 'The Red Party\'s turn \nMake your Choice\nThere are 10 actions you can take.\n\n\
1: Use the party\'s own newspaper to carry out Propaganda \nUncertainty: 9\nFollower Lost: 1 %\n\n\
2: Use the party\'s own radio stations to carry out Propaganda \nUncertainty: 8\nFollower Lost: 5 %\n\n\
3: Use the party\'s own television stations to carry out Propaganda \nUncertainty: 7\nFollower Lost: 7 %\n\n\
4: Use the party\'s official social network accounts to carry out Propaganda\nUncertainty: 6\nFollower Lost: 10 %\n\n\
5: Tour inflammatory political speeches in an area\nUncertainty: 5\nFollower Lost: 13 %\n\n\
6: Tour inflammatory political speeches in the whole country\nUncertainty: 4\nFollower Lost: 15 %\n\n\
7: Secretly interfering with the Blue Party\'s actions\nUncertainty: 3\nFollower Lost: 17 %\n\n\
8: Bribe the media to demonise the Blue Party\nUncertainty: 2\nFollower Lost: 20 %\n\n\
9: Assassinate important members of the Blue Party	\nUncertainty: 1.5\nFollower Lost: 40 %\n\n\
10: Intimidate the people to prevent the people from voting	\nUncertainty: 1\nFollower Lost: 50 %'

blue_choice_msg = 'The Blue Party\'s turn \nMake your Choice\nThere are 10 actions you can take. \n\n\
1: Use the party\'s own newspaper to encourage people to vote \nUncertainty: 8.5\nCost: 1\n\n\
2: Use the party\'s own radio stations to encourage people to vote \nUncertainty: 8\nCost: 2\n\n\
3: Use the party\'s own television stations to encourage people to vote \nUncertainty: 7.5\nCost: 3\n\n\
4: Use the party\'s official social network accounts to encourage people to vote \nUncertainty: 6\nCost: 4\n\n\
5: Advertise in the mainstream media to encourage people to vote \nUncertainty: 5.5\nCost: 5\n\n\
6: Tour political speeches in an area \nUncertainty: 5\nCost: 6\n\n\
7: Tour political speeches in the whole country \nUncertainty: 4.5\nCost: 7\n\n\
8: Promise people their freedom will be guaranteed \nUncertainty: 4\nCost: 8\n\n\
9: Promise people that the vote will be supervised to ensure fairness \nUncertainty: 3.5\nCost: 9\n\n\
10: Gather evidence to reveal the crimes of the Red Party \nUncertainty: 3\nCost: 10'

# INITIALISE COMPLETE

game_mode = ui.buttonbox(msg='Initialisaiton is complete.\n\nPlease select a game mode.',
                         title='Game Mode', choices=('Player VS Player', 'Player VS Computer', 'Computer VS Computer'))
if game_mode == 'Player VS Player':
    # Player VS Player
    # Take turns one by one
    while True:
        # Check energy level every turn
        if energy_level <= 0:
            game_over()

        round_counter = round_counter + 1  # round proceeds

        helper.print_green_data_before(green_data, round_counter)
        # green nodes interacts with green nodes
        game.green_interact(green_data, g)
        # output the status of all green nodes
        helper.print_green_data_after(green_data, round_counter)

        # The Red Party's turn
        while True:
            # red agent's followers are too little
            if len(follower_list) < red_actable['1']['follower_lost']:
                ui.msgbox(msg='The Red Party has no enough follower!')
                break

            red_choice = ui.buttonbox(
                msg=red_choice_msg,
                title='The Red Party\'s round {}'.format(round_counter),
                choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Check Status', 'Exit the Game'])
            if red_choice == '1' or red_choice == '2' or red_choice == '3' or red_choice == '4' or red_choice == '5' or red_choice == '6' or red_choice == '7' or red_choice == '8' or red_choice == '9' or red_choice == '10':
                red_act = red_choice
                if len(follower_list) < red_actable[red_act]['follower_lost']:
                    ui.msgbox(
                        msg='The Red Party does not has enough follower for this action')
                    continue
                game.red_interact(green_data, red_actable,
                                  red_act, follower_list)
                for y in range(red_actable[red_act]['follower_lost']):
                    # a random node to lost connection to
                    fl = random.randint(0, len(follower_list) - 1)
                    del follower_list[fl]
                # print(follower_list)
                follower_lost = follower_lost + \
                    red_actable[red_act]['follower_lost']
                break
            elif red_choice == 'Check Status':
                print_status()
            else:
                helper.confirm_exit()

        # The Blue Party's turn
        while True:
            blue_choice = ui.buttonbox(
                msg=blue_choice_msg,
                title='The Blue Party\'s round {}'.format(round_counter),
                choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Active a spy', 'Check Status', 'Exit the Game'])
            # Choice to interact with green team directly
            if blue_choice == '1' or blue_choice == '2' or blue_choice == '3' or blue_choice == '4' or blue_choice == '5' or blue_choice == '6' or blue_choice == '7' or blue_choice == '8' or blue_choice == '9' or blue_choice == '10':
                blue_act = blue_choice
                game.blue_interact(green_data, blue_actable, blue_act)
                energy_level = energy_level - \
                    blue_actable[blue_act]['energy_lost']  # lose energy
                break
            elif blue_choice == 'Active a spy':  # Choice to activate a grey spy
                if num_grey > 0:
                    # randomly choose a grey agent
                    pos = random.randint(0, len(grey_agents) - 1)
                    if grey_agents[pos] == 0:  # it is a red spy
                        red_act = '10'
                        # won't lose follower here
                        game.red_interact(
                            green_data, red_actable, red_act, follower_list)
                        del grey_agents[pos]  # that grey agent perish
                        num_grey = num_grey - 1  # Used spy bug fixed
                    else:  # it is a blue spy
                        blue_act = '10'  # the best one for blue agent
                        # won't lose energy
                        game.blue_interact(green_data, blue_actable, blue_act)
                        del grey_agents[pos]  # that grey agent perish
                        num_grey = num_grey - 1  # Used spy bug fixed
                    break

                else:
                    ui.msgbox(msg='All spy is active',
                              title='No grey available')
                    continue
            elif blue_choice == 'Check Status':
                print_status()
            else:
                helper.confirm_exit()

elif game_mode == 'Player VS Computer':
    player_party = ui.buttonbox(msg='Please choose the party you want to be.',
                                title='Choose Player\'s Party', choices=('The Red Party', 'The Blue Party'))
    if player_party == 'The Red Party':
        while True:
            # Check energy level every turn
            if energy_level <= 0:
                game_over()

            round_counter = round_counter + 1  # round proceeds
            helper.print_green_data_before(green_data, round_counter)
            # green nodes interacts with green nodes
            game.green_interact(green_data, g)
            # output the status of all green nodes
            helper.print_green_data_after(green_data, round_counter)

            # The Red Party(Player)'s turn
            while True:
                # red agent's followers are too little
                if len(follower_list) < red_actable['1']['follower_lost']:
                    ui.msgbox(msg='The Red Party has no enough follower!')
                    break

                red_choice = ui.buttonbox(
                    msg=red_choice_msg,
                    title='The Red Party\'s round {}'.format(round_counter),
                    choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Check Status', 'Exit the Game'])
                if red_choice == '1' or red_choice == '2' or red_choice == '3' or red_choice == '4' or red_choice == '5' or red_choice == '6' or red_choice == '7' or red_choice == '8' or red_choice == '9' or red_choice == '10':
                    red_act = red_choice
                    if len(follower_list) < red_actable[red_act]['follower_lost']:
                        ui.msgbox(
                            msg='The Red Party does not has enough follower for this action')
                        continue
                    game.red_interact(green_data, red_actable,
                                      red_act, follower_list)
                    for y in range(red_actable[red_act]['follower_lost']):
                        # a random node to lost connection to
                        fl = random.randint(0, len(follower_list) - 1)
                        del follower_list[fl]
                    # print(follower_list)
                    follower_lost = follower_lost + \
                        red_actable[red_act]['follower_lost']
                    break
                elif red_choice == 'Check Status':
                    print_status()
                else:
                    helper.confirm_exit()

            # Computer's turn
            while True:
                cont_ai = ui.ccbox(msg='This is computer\'s turn.\n\nPlease click the button to continue.',
                                   title='The Blue Party\'s round {}'.format(round_counter), choices=('Continue', 'Exit'))
                if cont_ai == True:

                    # print(blue_actable)
                    blue_choice = ba.blue_agent(
                        blue_actable, green_data, grey_agents, energy_level)
                    if blue_choice != '':
                        print('\nBlue AI choose {}'.format(blue_choice))
                    if blue_choice == 'activate':       # AI chose to activate grey agent
                        # randomly choose a grey agent
                        pos = random.randint(0, len(grey_agents) - 1)
                        if grey_agents[pos] == 0:  # it is a red spy
                            red_act = '10'       # the best one for red agent
                            # won't lose follower here
                            game.red_interact(
                                green_data, red_actable, red_act, follower_list)
                            del grey_agents[pos]  # that grey agent perish
                            num_grey = num_grey - 1  # Used spy bug fixed
                        else:  # it is a blue spy
                            blue_act = '10'      # the best one for blue agent
                            # won't lose energy
                            game.blue_interact(
                                green_data, blue_actable, blue_act)
                            del grey_agents[pos]  # that grey agent perish
                            num_grey = num_grey - 1  # Used spy bug fixed
                    elif blue_choice == '':
                        energy_level = 0
                        break
                    else:                     # AI chose to use an action
                        game.blue_interact(
                            green_data, blue_actable, blue_choice)
                        energy_level = energy_level - \
                            blue_actable[blue_choice]['energy_lost']  # lose energy
                    break
                elif cont_ai == False:
                    helper.confirm_exit()

    elif player_party == 'The Blue Party':
        while True:
            # Check energy level every turn
            if energy_level <= 0:
                game_over()

            round_counter = round_counter + 1  # round proceeds
            helper.print_green_data_before(green_data, round_counter)
            # green nodes interacts with green nodes
            game.green_interact(green_data, g)
            # output the status of all green nodes
            helper.print_green_data_after(green_data, round_counter)

            # computer's turn
            while True:
                cont_ai = ui.ccbox(msg='This is computer\'s turn.\n\nPlease click the button to continue.',
                                   title='The Red Party\'s round {}'.format(round_counter), choices=('Continue', 'Exit'))
                if cont_ai == True:

                    # red agent's followers are too little
                    if len(follower_list) < red_actable['1']['follower_lost']:
                        ui.msgbox(msg='The Red Party has no enough follower!')
                        break
                    else:
                        red_act = ra.red_agent(
                            red_actable, green_data, follower_list)
                        print('AI\'s choice is {}'.format(
                            red_act))  # ONLY FOR TEST
                        game.red_interact(
                            green_data, red_actable, red_act, follower_list)
                        for y in range(red_actable[red_act]['follower_lost']):
                            # a random node to lost connection to
                            fl = random.randint(0, len(follower_list) - 1)
                            del follower_list[fl]
                        # print(follower_list)
                        follower_lost = follower_lost + \
                            red_actable[red_act]['follower_lost']
                        break
                elif cont_ai == False:
                    helper.confirm_exit()

            # The Blue Party(Player)'s turn
            while True:
                blue_choice = ui.buttonbox(
                    msg=blue_choice_msg,
                    title='The Blue Party\'s round {}'.format(round_counter),
                    choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Active a spy', 'Check Status', 'Exit the Game'])
                # Choice to interact with green team directly
                if blue_choice == '1' or blue_choice == '2' or blue_choice == '3' or blue_choice == '4' or blue_choice == '5' or blue_choice == '6' or blue_choice == '7' or blue_choice == '8' or blue_choice == '9' or blue_choice == '10':
                    blue_act = blue_choice
                    game.blue_interact(green_data, blue_actable, blue_act)
                    energy_level = energy_level - \
                        blue_actable[blue_act]['energy_lost']  # lose energy
                    break
                elif blue_choice == 'Active a spy':  # Choice to activate a grey spy
                    if num_grey > 0:
                        # randomly choose a grey agent
                        pos = random.randint(0, len(grey_agents) - 1)
                        if grey_agents[pos] == 0:  # it is a red spy
                            red_act = '10'  # the best one for red agent
                            # won't lose follower here
                            game.red_interact(
                                green_data, red_actable, red_act, follower_list)
                            del grey_agents[pos]  # that grey agent perish
                            num_grey = num_grey - 1  # Used spy bug fixed
                        else:  # it is a blue spy
                            blue_act = '10'  # the best one for blue agent
                            # won't lose energy
                            game.blue_interact(
                                green_data, blue_actable, blue_act)
                            del grey_agents[pos]  # that grey agent perish
                            num_grey = num_grey - 1  # Used spy bug fixed
                        break

                    else:
                        ui.msgbox(msg='All spy is active',
                                  title='No grey available')
                        continue
                elif blue_choice == 'Check Status':
                    print_status()
                else:
                    helper.confirm_exit()


elif game_mode == 'Computer VS Computer':
    while True:
        # Check energy level every turn
        if energy_level <= 0:
            game_over()

        round_counter = round_counter + 1  # round proceeds

        # helper.print_green_data_before(green_data, round_counter)
        # green nodes interacts with green nodes
        game.green_interact(green_data, g)
        # output the status of all green nodes
        # helper.print_green_data_after(green_data, round_counter)

        # computer vs computer process: blue and red agents take turns one by one
        # Red Agent's Turn
        while True:
            # cont_ai = ui.ccbox(msg='This is computer\'s turn.\n\nPlease click the button to continue.',
            # title='The Red Party\'s round {}'.format(round_counter), choices=('Continue', 'Exit'))
            # if cont_ai == True:

            # red agent's followers are too little
            if len(follower_list) < red_actable['1']['follower_lost']:
                # ui.msgbox(msg='The Red Party has no enough follower!')
                break
            else:
                red_act = ra.red_agent(
                    red_actable, green_data, follower_list)
                print('\nRed AI\'s choice is {}'.format(
                    red_act))  # ONLY FOR TEST
                game.red_interact(green_data, red_actable,
                                  red_act, follower_list)
                for y in range(red_actable[red_act]['follower_lost']):
                    # a random node to lost connection to
                    fl = random.randint(0, len(follower_list) - 1)
                    del follower_list[fl]
                # print(follower_list)
                follower_lost = follower_lost + \
                    red_actable[red_act]['follower_lost']
                break
            # elif cont_ai == False:
            # helper.confirm_exit()

        # Blue Agent's Turn
        while True:
            # cont_ai = ui.ccbox(msg='This is computer\'s turn.\n\nPlease click the button to continue.',
            # title='The Blue Party\'s round {}'.format(round_counter), choices=('Continue', 'Exit'))
            # if cont_ai == True:
            # print(blue_actable)

            blue_choice = ba.blue_agent(
                blue_actable, green_data, grey_agents, energy_level)
            if blue_choice != '':
                print('\nBlue AI choose {}'.format(blue_choice))
            if blue_choice == 'activate':  # AI chose to activate grey agent
                # randomly choose a grey agent
                pos = random.randint(0, len(grey_agents) - 1)
                if grey_agents[pos] == 0:  # it is a red spy
                    red_act = '10'  # the best one for red agent
                    # won't lose follower here
                    game.red_interact(
                        green_data, red_actable, red_act, follower_list)
                    del grey_agents[pos]  # that grey agent perish
                    num_grey = num_grey - 1  # Used spy bug fixed
                else:  # it is a blue spy
                    blue_act = '10'  # the best one for blue agent
                    # won't lose energy
                    game.blue_interact(green_data, blue_actable, blue_act)
                    del grey_agents[pos]  # that grey agent perish
                    num_grey = num_grey - 1  # Used spy bug fixed
            elif blue_choice == '':
                energy_level = 0
                break
            else:  # AI chose to use an action
                game.blue_interact(green_data, blue_actable, blue_choice)
                energy_level = energy_level - \
                    blue_actable[blue_choice]['energy_lost']  # lose energy
            break
       # elif cont_ai == False:
            # helper.confirm_exit()