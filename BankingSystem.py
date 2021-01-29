import random
import sys
import sqlite3


def luhn_alg(num):
    digits = list(map(int, list(num)))
    digits = [digits[k] * 2 if k % 2 == 0 else digits[k] for k in range(len(digits))]
    digits = [num - 9 if num > 9 else num for num in digits]
    last_digit = 10 - sum(digits) % 10
    if last_digit == 10:
        return 0
    else:
        return last_digit


def check_num_by_luhn(num):
    digits = list(map(int, list(num)))
    digits = [digits[k] * 2 if k % 2 == 0 else digits[k] for k in range(len(digits))]
    digits = [num - 9 if num > 9 else num for num in digits]
    if (sum(digits) % 10) == 0:
        return True
    else:
        return False


def get_number():
    num = '400000'
    for i in range(9):
        num = num + str(random.randint(0, 9))
    last_digit = luhn_alg(num)
    return num + str(last_digit)


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
        self.create_account()
        print('\nYour card has been created\nYour card number:\n' + self.number + \
              '\nYour card PIN\n' + self.pin + '\n')

    def create_account(self):
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        cur.execute('insert into card values ((select count(*) from card) + 1, {}, {}, 0)'.format(self.number, self.pin))
        conn.commit()


class BankingSystem:
    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.cur.execute('drop table if exists card')
        self.cur.execute('create table card(id INTEGER, number  TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
        self.conn.commit()
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
            self.cabinet(numbers, code)

    def cabinet(self, num, pin):
        print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit')
        k = int(input())
        if k == 1:
            self.cur.execute('select balance from card where number = {}'.format(num))
            print('\nBalance: ', self.cur.fetchone()[0], '\n')
            self.cabinet(num, pin)
        elif k == 2:
            print('Enter income:')
            income = int(input())
            self.cur.execute('update card set balance = balance + {0} where number={1}'.format(income, num))
            self.conn.commit()
            print('Income was added!\n')
            self.cabinet(num, pin)
        elif k == 3:
            self.transfer(num, pin)
        elif k == 4:
            self.cur.execute('delete from card where number={}'.format(num))
            self.conn.commit()
            print('\nThe account has been closed!\n')
            self.menu()
        elif k == 5:
            print('\nYou have successfully logged out!\n')
            self.menu()
        elif k == 0:
            print('\nBye!\n')
            sys.exit()
        else:
            self.error()
            self.cabinet(num, pin)

    def transfer(self, num_own, pin_own):
        print('Enter card number:')
        to_num = input()
        if to_num == num_own:
            print('You can\'t transfer money to the same account!')
            self.cabinet(num_own, pin_own)
        if not check_num_by_luhn(to_num):
            print('Probably you made a mistake in the card number. Please try again!\n')
            self.cabinet(num_own, pin_own)
        self.cur.execute('select number from card')
        card_in_db = [account[0] for account in self.cur.fetchall()]
        if to_num not in card_in_db:
            print('Such a card does not exist.\n')
            self.cabinet(num_own, pin_own)
        print('Enter how much money you want to transfer:')
        money = int(input())
        if not self.check_balance(num_own, money):
            print('Not enough money!\n')
            self.cabinet(num_own, pin_own)
        else:
            self.transaction(num_own, to_num, money)
            self.cabinet(num_own, pin_own)

    def transaction(self, from_n, to_n, money):
        self.cur.execute('update card set balance = balance - {0} where number={1}'.format(money, from_n))
        self.conn.commit()
        self.cur.execute('update card set balance = balance + {0} where number={1}'.format(money, to_n))
        self.conn.commit()
        print('Success!\n')

    def check_balance(self, num, money):
        self.cur.execute('select balance from card where number={}'.format(num))
        balance = self.cur.fetchall()[0][0]
        if balance < money:
            return False
        else:
            return True

    def error(self):
        print('\nОшибка ввода\n')


if __name__ == '__main__':
    BankingSystem()
