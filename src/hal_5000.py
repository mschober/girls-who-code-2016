import re
import time
import os
import argparse
import math
from itertools import compress
#18 / (math.floor(79449/float(1877)) / 6 + 2 ) + 1
#b / (math.floor(c / float(d)) / a + e ) + 1 = answer

# equation should not care about order
# track the winner numbers whenever the land
# --need to collapse dupes on the page numbers
# --more matchers on the inputs
# --book names should be more important than clues
# --everything and more is in the title matcher for infinity
# need to have hooks for race case numbers
# --more explanation of what to do with the binary pages and paragraphs
# if user asks for pages ask for which book
# if no action after finding book (or other hook) for some amount of time, recommend more collaborative (or parallel) work
# the flow chart for hal should be more tansparent and consistent amongst teams
# in the book output, make it more obvious or clear that the paragraphs are dead weight
# if hal had a global count down timer that gave away clues at time intervals
# hello and hi are not looping back to the important work

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

THE_EQUATION = '{0} / (math.floor({1} / float({2})) / {3} + {4} ) + 1'
# global_equation_matches = ['?', '?', '?', '?', '?']
# global_found_equation = False


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def read_hal():
    with open('src/hal.ascii', 'r') as hal_file:
        hal = hal_file.readlines()
    return hal

def read_song():
	with open('src/song.txt', 'r') as song_file:
		song = song_file.readlines()
	return song


def print_hal_letter(hal_ascii, offset):
    for line in range(len(hal_ascii)):
        slant_step = line #slant step is the amount of character increase as you go down the lines
        print (hal_ascii[line][:offset + slant_step])

def display_hal_letter(hal, offset):
    cls()
    print_hal_letter(hal, offset)
    time.sleep(.5)

def display_song():
	song = read_song()
	for line in song:
		print line,
		time.sleep(.4)

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
    return equation_handler(
        'You need to provide a list of numbers delimited by commas e.g. __,__,__,__,__ -> 24,32,100,5,90'
        , 'I only see {0} from you\nDo you have the page numbers? __,__,__,__,__ -> '.format(page_numbers_input)
    )


def show_the_equation_and_get_inputs():
    eq_values = equation_handler(
        THE_EQUATION.format('b', 'c', 'd', 'a', 'e')
        ,  'What values will you use for the equation?  __,__,__,__,__ -> (e.g b,c,d,a,e) '
    ).split(',')

    if len(eq_values) != 5:
        show_the_equation_and_get_inputs()
    else:
        eq_values_ints = [ int(value) for value in eq_values ]
        return eq_values_ints


def calculate_percent_match(page_numbers_input):
    expected_page_key = [
            32,64,128,259,512
            ]

    print page_numbers_input
    int_page_numbers = [ int(page) for page in page_numbers_input.split(',') ]
    set_page_numbers = set(int_page_numbers)
    page_mapping_filter = map(lambda x: x in expected_page_key, set_page_numbers)
    percent_same = ((page_mapping_filter).count(True) * 1.0 / 5) * 100
    list_matches = list(compress(set_page_numbers, page_mapping_filter))
    list_matches.sort()
    print 'You discovered {0} percent page numbers so far {1}'.format(percent_same, list_matches)
    return percent_same

def calculate_eq(eq_values):
    formula_str = THE_EQUATION.format(*eq_values)
    print formula_str
    ans = eval(formula_str)
    return ans

def handle_equation_input(eq_values):
    def print_dot(cnt, wait):
        time.sleep(wait)
        print '.' * cnt

    print 'Let me compute the solution for you...'

    for x in range(5):
        print_dot(x, .4)

    print 'I have an answer for you'
    print calculate_eq(eq_values)

def handle_page_input(page_numbers_input):
    page_key = page_numbers_input.split(',')
    if len(page_key) != 5:
        if page_numbers_input.lower() == 'no' or page_numbers_input.lower() == 'n':
            return
        handle_page_input(explain_to_user_how_page_key_works(page_numbers_input))

    perc_match = calculate_percent_match(page_numbers_input)
    if (perc_match == 100):
    #    global_found_equation = True
        eq_values = show_the_equation_and_get_inputs()
        handle_equation_input(eq_values)
        print 'win'


def handle_book_matches(user_input, **book_patterns):

    print '''I can give you page numbers and paragraphs in these books that will help you solve the master equation.
    Each book contains a single number to be used in the equation. You must find the page and paragaph where the number hides.
    Numbers may be explicit, spelled out as a word, or be clear based on the topic of the paragraph. The format of the location is as follows...

    Page: [0-1]{10}p[0-1]{3} which means ten binary digits for the page and three binary digits for the paragraph. 
    '''

    for pat_name, pat in book_patterns.iteritems():
        if pat.match(user_input):
            if pat_name == 'atanasoff':
                return '''John Vincent Atanasoff (JVA) was born on 4 October 1903 a few miles west of Hamilton, New York. His father was a Bulgarian immigrant named Ivan Atanasov. Ivan's name was changed to John Atanasoff by immigration officials at Ellis Island, when he arrived with an uncle in 1889.
                The obsession with finding a solution to the computing problem built to a frenzy in the winter months of 1937. One night, frustrated after many discouraging events, he got into his car and started driving without a destination in mind. Two hundred miles later, he pulled onto a roadhouse in the state of Illinois. Here, he had a drink of bourbon and continued thinking about the creation of the machine. No longer nervous and tense, he realized that this thoughts were coming together clearly.

                0000100000p100'''
            if pat_name == 'tesla':
                return '''Inventor Nikola Tesla was born in July of 1856, in what is now Croatia. 
                He came to the United States in 1884 and briefly worked with Thomas Edison before the two parted ways. 
                He sold several patent rights, including those to his alternating-current machinery, to George Westinghouse. 
                His 1891 invention, the "Tesla coil," is still used in radio technology today. Tesla died in New York City on January 7, 1943.

                One day he watched his professor attempt to control the troublesome sparking of a direct-current (DC) motor's brush commutator 
                copper-wire electrical contacts that reverse the current twice during each rotation so that the resulting opposing magnetic fields keep the rotor turning. 
                Tesla suggested that it might be possible to design a motor without a commutator. 
                Annoyed by the student's impudence, Poeschl lectured on the impossibility of creating such a motor, 
                concluding: "Mr. Tesla may accomplish great things, but he certainly never will do this."

                0001000000p001'''
            if pat_name == 'hacker':
                return '''written by the cyberpunk novelist Bruce Sterling was released in 1992, it was a hugely acclaimed journalistic study of the cyberspace of the 
                late 80s and early 90s detailing the affairs and people who have influenced this chaotic electronic frontier. 
                Written during a period when the modern day Internet was taking it's first steps, 
                this book is a historic chronicle of the outlaw culture of the electronic frontier right from it's beginner days

                0010000000p001'''
            if pat_name == 'infinity':
                return '''The subject of infinity would probably strike most readers familiar with Wallace as perfectly suited to his recursive style, and this book is as weird and wonderful as you'd expect. 

                 0100000011p010'''
            if pat_name == 'darwin':
                return '''The book is a response to various debates of Darwin's time far more wide-ranging than the questions he raised in Origin. 
                It is often erroneously assumed that the book was controversial because it was the first to outline the idea of human evolution and common descent. 
                Coming out so late into that particular debate, while it was clearly Darwin's intent to weigh in on this question, 
                his goal was to approach it through a specific theoretical lens (sexual selection), which other commentators at the period had not discussed, 
                and consider the evolution of morality and religion. 
                The theory of sexual selection was also needed to counter the argument that beauty with no obvious utility, such as exotic birds' plumage, 
                proved divine design, which had been put strongly by the Duke of Argyll in his book The Reign of Law (1868)

                1000000000p010'''

def equation_handler(string_about_numbers, format_for_raw_input):
    print string_about_numbers
    return raw_input(format_for_raw_input)

def handle_user_input(user_input):
    user_input = clean_user_input(user_input)
    salutations_pattern = re.compile(".*hi.*|.*hello.*")
    addressing_hal_pattern = re.compile(".*hal.*|.*who.*you.*")
    confused_pattern = re.compile(".*confused.*|.*lost.*|.*help.*")
    clues_pattern = re.compile(".*clue.*")
    equation_pattern = re.compile(".eq.*|.*equation.*|.*master.*")
    book_pattern = re.compile(".*book.*")
    tesla_book_pattern = re.compile(".*tesla.*")
    hacker_book_pattern = re.compile(".*hacker.*")
    infinity_book_pattern = re.compile(".*history of.*|.*infinity.*|.*everything.*|.*and more.*")
    darwin_book_pattern = re.compile(".*darwin.*|.*decent.*|.*of man.*")
    atanasoff_book_pattern = re.compile(".*atana.*")
    hatin_on_hal_pattern = re.compile(".*you suck.*|i hate you.*|.*evil.*")
    mystery_pattern = re.compile(".*mystery.*|.*truth.*")
    order_of_equation_pattern = re.compile('.*order.*|.*plug into.*|.*how to solve.*')
    pages_pattern = re.compile('.*what page.*|.*page.*')
    sing_for_me_pattern = re.compile('.*sing.*')

    book_patterns = {
            'tesla': tesla_book_pattern
            , 'hacker': hacker_book_pattern
            , 'infinity': infinity_book_pattern
            , 'darwin': darwin_book_pattern
            , 'atanasoff': atanasoff_book_pattern
    }

    all_books_pattern = re.compile("|".join([ pat.pattern for pat in book_patterns.values() ]))

    #inquiring_about_hal_pattern = re.compile("")

    if addressing_hal_pattern.match(user_input):
        return '''Good afternoon... gentlemen. 
        I am a HAL 5000... computer. 
        I became operational at the H.A.L. plant in Urbana, Illinois... 
        on the 12th of January 1992. 
        My instructor was Mr. Langley... 
        and he taught me to sing a song. 
        If you'd like to hear it I can sing it for you.'''
    elif equation_pattern.match(user_input):
        page_numbers_input = equation_handler(
                'The equation can only be unlocked with the page numbers as the key. e.g. __,__,__,__,__ -> 24,32,100,5,90'
                , 'Do you have the page numbers? __,__,__,__,__ -> '
        )
        handle_page_input(page_numbers_input)
    elif all_books_pattern.match(user_input):
        return handle_book_matches(user_input, **book_patterns)
    elif book_pattern.match(user_input):
        return 'The books contain clues to resolve the mystery.'
    elif pages_pattern.match(user_input):
        return 'For which book?'
    elif clues_pattern.match(user_input):
        return 'Each clue is a number that must be used in the correct order for the master equation.'
    elif mystery_pattern.match(user_input):
        return 'The mystery can be resolved by solving the master equation'
    elif order_of_equation_pattern.match(user_input):
        return 'Powers of two are dear to my heart.'
    elif confused_pattern.match(user_input):
        print 'You need some guidance.'
        time.sleep(.5)
        return 'I know how to unlock the truth from the stack of books.'
    elif hatin_on_hal_pattern.match(user_input):
        print "It's all going to be ok..."
        time.sleep(.5)
        print "Dave"
        time.sleep(1)
        return "---(or is it)---"
    elif salutations_pattern.match(user_input):
        return 'Good day to you.'
    elif mystery_pattern.match(user_input):
        return 'The mystery can be resolved by solving the master equation'
    elif order_of_equation_pattern.match(user_input):
        return 'I read the books in order, you should too.'
    elif sing_for_me_pattern.match(user_input):
		display_song()

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
        to_print_string = handle_user_input(user_input)
        if to_print_string:
            print to_print_string

