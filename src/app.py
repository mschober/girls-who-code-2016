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

def print_hal_letter(letter):
    cls()
    print letter
    print
    time.sleep(1)


def read_hal():
    with open('src/hal.ascii', 'r') as hal_file:
        hal = hal_file.readlines()
    return hal

def print_hal(hal, offset):
    for i in range(len(hal)):
        print (hal[i][:offset + i])

def print_hal_letter(hal, offset):
    cls()
    print_hal(hal, offset)
    time.sleep(1)

if __name__ == '__main__':
    hal = read_hal()
    print_hal_letter(hal, HAL_H)
    print_hal_letter(hal, HAL_HA)
    print_hal_letter(hal, HAL_HAL)
    print_hal_letter(hal, HAL_HAL__)
    print_hal_letter(hal, HAL_HAL__5)
    print_hal_letter(hal, HAL_HAL_50)
    print_hal_letter(hal, HAL_HAL_500)
    print_hal_letter(hal, HAL_HAL_5000)
    print_hal_letter(hal, HAL_HAL_5000_DOT)
    print_hal_letter(hal, HAL_HAL_5000_DOT_DOT)
    print_hal_letter(hal, HAL_HAL_5000_DOT_DOT_DOT)
