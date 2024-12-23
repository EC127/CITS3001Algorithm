import easygui as ui
import sys


def get_vote_people(green_data):
    count = 0
    for i in green_data:
        if green_data[i]['opinion'] == 1:
            count += 1
    return count


def confirm_exit():
    if ui.ccbox(msg='You are exiting the game! \nAre you sure?', title='Confirm', choices=('Yes', 'No')):
        sys.exit(0)
    # end if Exit is chosen


def game_result(green_data):
    num_green = len(green_data)
    voter = 0
    for i in green_data:
        if green_data[i]['opinion'] == 1:
            voter += 1
    if voter > - voter:
        return 'Blue win!'
    elif voter < num_green - voter:
        return 'Red win!'
    elif voter == num_green - voter:
        return 'It is a Draw!'


def print_green_data_before(green_data, round_counter):
    sum = 0
    for i in green_data:
        sum = sum + green_data[i]['uncertainty']
    avg_uncer = sum/len(green_data)

    message = 'Round {} \nBefore people interact: \n\n'.format(
        round_counter) + 'People who wants to vote: {}\n\nPeople who will not vote: {}\n\nAverage uncertainty: {}'.format(
        get_vote_people(green_data), len(green_data) - get_vote_people(green_data), avg_uncer)

    ui.msgbox(msg=message,
              title='Status View (Before People Interact)', ok_button='Continue')


def print_green_data_after(green_data, round_counter):
    sum = 0
    for i in green_data:
        sum = sum + green_data[i]['uncertainty']
    avg_uncer = sum/len(green_data)

    message = 'Round {} \nAfter people interact: \n\n'.format(
        round_counter) + 'People who wants to vote: {}\n\nPeople who will not vote: {}\n\nAverage uncertainty: {}'.format(
        get_vote_people(green_data), len(green_data) - get_vote_people(green_data), avg_uncer)

    ui.msgbox(msg=message,
              title='Status View (After People Interact)', ok_button='Continue')