import re
import time
import os

META_FOR_HAL = '''
site: http://patorjk.com/software/taag/#p=display&f=Slant%20Relief&t=HAL%205000...
text: HAL 5000...
font: Slant Relief
'''

HAL_HAL_5000_DOT_DOT_DOT = 152

HAL_HAL_5000_DOT_DOT = 144

HAL_HAL_5000_DOT = 138

HAL_HAL_5000 = 132

HAL_HAL_500 = 116

HAL_HAL_50 = 100

HAL_HAL__5 = 85

HAL_HAL__ = 65

HAL_HAL = 55

HAL_HA = 35

HAL_H = 19


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def read_hal():
    with open('src/hal.ascii', 'r') as hal_file:
        hal = hal_file.readlines()
    return hal

def print_hal_letter(hal_ascii, offset):
    for line in range(len(hal_ascii)):
        slant_step = line #slant step is the amount of character increase as you go down the lines
        print (hal_ascii[line][:offset + slant_step])

def display_hal_letter(hal, offset):
    cls()
    print_hal_letter(hal, offset)
    time.sleep(1)


def print_hal():
    display_hal_letter(hal, HAL_H)
    display_hal_letter(hal, HAL_HA)
    display_hal_letter(hal, HAL_HAL)
    display_hal_letter(hal, HAL_HAL__)
    display_hal_letter(hal, HAL_HAL__5)
    display_hal_letter(hal, HAL_HAL_50)
    display_hal_letter(hal, HAL_HAL_500)
    display_hal_letter(hal, HAL_HAL_5000)
    display_hal_letter(hal, HAL_HAL_5000_DOT)
    display_hal_letter(hal, HAL_HAL_5000_DOT_DOT)
    display_hal_letter(hal, HAL_HAL_5000_DOT_DOT_DOT)


def handle_user_input(user_input):
    user_input = clean_user_input(user_input)
    salutations_pattern = re.compile(".*hi.*|.*hello.*")
    addressing_hal_pattern = re.compile(".*hal.*")
    open_ended_question_pattern = re.compile(".*what.*")
    confused_pattern = re.compile(".*confused.*|.*lost.*")
    books_pattern = re.compile(".*book.*")
    inquiring_about_hal_pattern = re.compile(".*who.*you.*")

    if user_input == '':
        print 'you seem confused'
    elif books_pattern.match(user_input):
        print 'explain about the books'
    elif addressing_hal_pattern.match(user_input):
        print 'some reply from hal'
    elif salutations_pattern.match(user_input):
        print 'something about hi'
    elif open_ended_question_pattern.match(user_input):
        print 'you need some guidance'
    elif confused_pattern.match(user_input):
        print 'its easy to get lost'
    elif inquiring_about_hal_pattern.match(user_input):
        print 'hals an important scary guys'


def clean_user_input(user_input):
    user_input = user_input.strip()
    user_input = user_input.lower()
    return user_input


if __name__ == '__main__':
    hal = read_hal()
    # print_hal()
    display_hal_letter(hal, HAL_HAL_5000_DOT_DOT_DOT)

    print
    while True:
        user_input = raw_input('> ')
        handle_user_input(user_input)

