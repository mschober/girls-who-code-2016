import re
import time
import os
import argparse
from itertools import compress


parser = argparse.ArgumentParser()
parser.add_argument('--hal', dest='hal', action='store_true')
args = parser.parse_args()

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
    time.sleep(.5)


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

def explain_to_user_how_page_key_works(page_numbers_input):
    print '''You need to provide a list of numbers delimited by commas e.g. __,__,__,__,__ -> 24,32,100,5,90
            I only see {0} from you'''.format(page_numbers_input)


def calculate_percent_match(page_numbers_input):
    expected_page_key = [
            10,11,12,13,14
            ]

    page_numbers_ints = [ int(page) for page in page_numbers_input.split(',') ]
    page_mapping_filter = map(lambda x: x in expected_page_key, page_numbers_ints)
    percent_same = ((page_mapping_filter).count(True) * 1.0 / 5) * 100
    print 'You discovered {0} percent page numbers so far {1}'.format(percent_same, list(compress(page_numbers_ints, page_mapping_filter)))
    return percent_same

def handle_page_input(page_numbers_input):
    page_key = page_numbers_input.split(',')
    if len(page_key) != 5:
        explain_to_user_how_page_key_works(page_numbers_input)
        return

    perc_match = calculate_percent_match(page_numbers_input)
    if (perc_match == 100):
        print 'win'


def handle_user_input(user_input):
    user_input = clean_user_input(user_input)
    salutations_pattern = re.compile(".*hi.*|.*hello.*")
    addressing_hal_pattern = re.compile(".*hal.*|.*who.*you.*")
    open_ended_question_pattern = re.compile(".*what.*")
    confused_pattern = re.compile(".*confused.*|.*lost.*|.*help.*")
    clues_pattern = re.compile(".*clue.*")
    equation_pattern = re.compile(".eq.*|.*equation.*")
    books_pattern = re.compile(".*book.*")
    #inquiring_about_hal_pattern = re.compile("")

    if addressing_hal_pattern.match(user_input):
        print '''Good afternoon... gentlemen. 
        I am a HAL 5000... computer. 
        I became operational at the H.A.L. plant in Urbana, Illinois... 
        on the 12th of January 1992. 
        My instructor was Mr. Langley... 
        and he taught me to sing a song. 
        If you'd like to hear it I can sing it for you.'''
    elif books_pattern.match(user_input):
        print 'The books contain clues to resolve the mystery.'
    elif clues_pattern.match(user_input):
        print 'Each clue is a number that must be used in the correct order for the master equation.'
    elif equation_pattern.match(user_input):
        print 'The equation can only be unlocked with the page numbers as the key. e.g. __,__,__,__,__ -> 24,32,100,5,90'
        page_numbers_input = raw_input('Do you have the page numbers? __,__,__,__,__ -> ')
        handle_page_input(page_numbers_input)
    elif salutations_pattern.match(user_input):
        print 'Good day to you.'
    elif open_ended_question_pattern.match(user_input):
        print 'you need some guidance'
    elif confused_pattern.match(user_input):
        print 'I know the secrets of the mysteries and how to unlock the truth from the stack of books.'


def clean_user_input(user_input):
    user_input = user_input.strip()
    user_input = user_input.lower()
    return user_input


if __name__ == '__main__':
    hal = read_hal()
    if args.hal:
        print_hal()
        display_hal_letter(hal, HAL_HAL_5000_DOT_DOT_DOT)

    print
    while True:
        user_input = raw_input('> ')
        handle_user_input(user_input)

