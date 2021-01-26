import random
import sys


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
        print('\nYour card has been created\nYour card number:\n' + self.number + \
              '\nYour card PIN\n' + self.pin + '\n')


class BankingSystem:

    def __init__(self):
        self.menu()

    def menu(self):
        print('1. Create an account\n2. Log into account\n0. Exit')
        k = int(input())
        if k == 0:
            print('\nBye!\n')
            sys.exit()
        elif k == 1:
            self.create()
        elif k == 2:
            self.login()
        else:
            self.error()
            self.menu()

    def create(self):
        Card()
        self.menu()

    def login(self):
        print('\nEnter your card number:')
        numbers = input()
        print('Enter your PIN:')
        code = input()
        if (numbers not in Card.all_numbers.keys()) or (Card.all_numbers[numbers] != code):
            print('\nWrong card number or PIN!\n')
            self.menu()
        else:
            print('\nYou have successfully logged in!\n')
            self.cabinet()

    def cabinet(self):
        print('1. Balance\n2. Log out\n0. Exit')
        k = int(input())
        if k == 1:
            print('\nBalance: 0\n')
            self.cabinet()
        elif k == 2:
            print('\nYou have successfully logged out!\n')
            self.menu()
        elif k == 0:
            print('\nBye!\n')
            sys.exit()
        else:
            self.error()
            self.cabinet()

    def error(self):
        print('\nОшибка ввода\n')



if __name__ == '__main__':
    BankingSystem()



