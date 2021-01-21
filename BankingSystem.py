import random


def get_number():
    num = '400000'
    for i in range(10):
        num = num + str(random.randint(0, 9))
    return num


def get_pin():
    pin = ''
    for i in range(4):
        pin = pin + str(random.randint(0, 9))
    return pin


class Card:
    all_numbers = {}

    def __init__(self):
        self.number = get_number()
        while self.number in Card.all_numbers.keys():
            self.number = get_number()
        self.pin = get_pin()
        Card.all_numbers.update({self.number: self.pin})
        print('Your card has been created\nYour card number:\n' + self.number, \
              '\nYour card PIN\n' + self.pin)

if __name__ == '__main__':
    print('1. Create an account\n2. Log into account\n0. Exit')
    n = int(input())
    while n != 0:
        if n == 1:
            new_user = Card()
        elif n == 2:
            print('Enter your card number:')
            numbers = input()
            print('Enter your PIN:')
            code = input()
            if (numbers not in Card.all_numbers.keys()) or (Card.all_numbers[numbers] != code):
                print('Wrong card number or PIN!')
            else:
                print('\nYou have successfully logged in!\n')
                print('1. Balance\n2. Log out\n0. Exit')
                k = int(input())
                while k != 0 and k != 2:
                    if k == 1:
                        print('Balance: 0')
                        print('1. Balance\n2. Log out\n0. Exit')
                        k = int(input())
                if k == 2:
                    print('\nYou have successfully logged out!')
                if k == 0:
                    n = 0
        if n == 0:
            break
        else:
            print('\n1. Create an account\n2. Log into account\n0. Exit')
            n = int(input())



