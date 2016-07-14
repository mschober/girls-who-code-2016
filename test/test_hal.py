from unittest import TestCase
from src.hal_5000 import handle_user_input

class TestHal5000(TestCase):
#    salutations_pattern = re.compile(".*hi.*|.*hello.*")
#    user_input = clean_user_input(user_input)
#    addressing_hal_pattern = re.compile(".*hal.*|.*who.*you.*")
#    confused_pattern = re.compile(".*confused.*|.*lost.*|.*help.*")
#    clues_pattern = re.compile(".*clue.*")
#    equation_pattern = re.compile(".eq.*|.*equation.*|.*master.*")
#    book_pattern = re.compile(".*book.*")
#    tesla_book_pattern = re.compile(".*tesla.*")
#    hacker_book_pattern = re.compile(".*hacker.*")
#    infinity_book_pattern = re.compile(".*history of.*|.*infinity.*|.*everything.*|.*and more.*")
#    darwin_book_pattern = re.compile(".*darwin.*|.*decent.*|.*of man.*")
#    atanasoff_book_pattern = re.compile(".*atana.*")
#    hatin_on_hal_pattern = re.compile(".*you suck.*|i hate you.*|.*evil.*")
#    mystery_pattern = re.compile(".*mystery.*|.*truth.*")
#    order_of_equation_pattern = re.compile('.*order.*|.*plug into.*|.*how to solve.*')
#    pages_pattern = re.compile('.*what pages.*|.*pages.*')



    def test_user_input(self):
        user_inputs = {
                  'hello': 'Good day to you.'
                , 'hal': '''Good afternoon... gentlemen. 
        I am a HAL 5000... computer. 
        I became operational at the H.A.L. plant in Urbana, Illinois... 
        on the 12th of January 1992. 
        My instructor was Mr. Langley... 
        and he taught me to sing a song. 
        If you'd like to hear it I can sing it for you.'''
                , 'confused': 'You need some guidance.'
                , 'clue': 'Each clue is a number that must be used in the correct order for the master equation.'
                #, 'equation': 'The books contain clues to resolve the mystery.'
                , 'book': 'The books contain clues to resolve the mystery.'
                #, 'tesla': 'The books contain clues to resolve the mystery.'
                #, 'hacker': 'The books contain clues to resolve the mystery.'
                #, 'everything': 'The books contain clues to resolve the mystery.'
                #, 'decent': 'The books contain clues to resolve the mystery.'
                #, 'atanasoff': 'The books contain clues to resolve the mystery.'
                #, 'hate': 'The books contain clues to resolve the mystery.'
                , 'mystery': 'The mystery can be resolved by solving the master equation'
                , 'order': 'Powers of two are dear to my heart.'
                , 'pages': 'For which book?'
        }

        for input, reply in user_inputs.iteritems():
            #self.assertEquals(input, reply)
            self.assertEquals(reply, handle_user_input(input), "Key: {0}, for output '{1}'".format(input, handle_user_input(input)))
