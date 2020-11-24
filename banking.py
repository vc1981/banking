# Write your code here
import random
import sqlite3
from os import path


def create_account():
    global bank_accounts
    global bank_balance
    print('Your card has been created\n'
          'Your card number:')
    generated_account = generate_account()
    generated_pin = generate_pin()
    print(generated_account)
    print('Your card PIN:')
    print(generated_pin)
    db_add(int(generated_account), int(generated_pin))


def validate_bank_account(bank_account):
    digits = list(bank_account)
    digit = 0
    digits_sum = 0

    while digit < 15:
        if digit == 0 or digit % 2 == 0:
            digits[digit] = int(digits[digit]) * 2
            if digits[digit] >= 10:
                digits[digit] = digits[digit] - 9
        else:
            digits[digit] = int(digits[digit])
        digits_sum += int(digits[digit])
        digit += 1

    if (10 - (digits_sum % 10)) == 10:
        crc = 0
    else:
        crc = (10 - (digits_sum % 10))

    if digits[15] == str(crc):
        validation = True
    else:
        validation = False

    return validation


def generate_account():
    bank_account = '400000' + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) \
                        + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) \
                        + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) \
                        + str(random.randrange(0, 9))

    digits = list(bank_account)
    digit = 0
    digits_sum = 0

    while digit < 15:
        if digit == 0 or digit % 2 == 0:
            digits[digit] = int(digits[digit]) * 2
            if digits[digit] >= 10:
                digits[digit] = digits[digit] - 9
        else:
            digits[digit] = int(digits[digit])
        digits_sum += int(digits[digit])
        digit += 1

    if (10 - (digits_sum % 10)) == 10:
        digits.append(0)
    else:
        digits.append(10 - (digits_sum % 10))
    bank_account += str(digits[15])

    return bank_account


def generate_pin():
    return str(random.randrange(0, 9)) + str(random.randrange(0, 9)) + str(random.randrange(0, 9)) \
           + str(random.randrange(0, 9))


def log_into_account():
    global bank_accounts
    global user_input
    print('\n'
          'Enter your card number:')
    user_account = int(input())
    print('Enter your PIN:')
    user_pin = int(input())
    # if user_account in bank_accounts and user_pin == bank_accounts.get(user_account):
    if db_account_auth(user_account, user_pin) == 1:
        print('\n'
              'You have successfully logged in!\n'
              '\n'
              '1. Balance\n'
              '2. Add income\n'
              '3. Do transfer\n'
              '4. Close account\n'
              '5. Log out\n'
              '0. Exit')
        user_input_account = input()
        while user_input_account != 0:
            if user_input_account == '1':
                print('Income was added!'
                      '\n'
                      'Balance:' + str(db_balance_query(user_account, user_pin)) + '\n'
                      '\n'
                      '1. Balance\n'
                      '2. Add income\n'
                      '3. Do transfer\n'
                      '4. Close account\n'
                      '5. Log out\n'
                      '0. Exit')
                user_input_account = input()
            if user_input_account == '2':
                print('Enter income:')
                income = input()
                db_add_income(user_account, income)
                print('\n'
                      '1. Balance\n'
                      '2. Add income\n'
                      '3. Do transfer\n'
                      '4. Close account\n'
                      '5. Log out\n'
                      '0. Exit')
                user_input_account = input()
            if user_input_account == '3':
                print('Transfer\n'
                      'Enter card number:')
                transfer_account = input()
                if validate_bank_account(transfer_account):
                    if db_check_account(transfer_account):
                        print('Enter how much money you want to transfer:')
                        transfer = input()
                        if int(transfer) < int(db_balance_query(user_account, user_pin)):
                            db_add_income(transfer_account, transfer)
                            db_deduct_balance(user_account, transfer)
                            print('Success!\n'
                                  '\n'
                                  '1. Balance\n'
                                  '2. Add income\n'
                                  '3. Do transfer\n'
                                  '4. Close account\n'
                                  '5. Log out\n'
                                  '0. Exit')
                            user_input_account = input()
                        else:
                            print('Not enough money!\n'
                                  '\n'
                                  '1. Balance\n'
                                  '2. Add income\n'
                                  '3. Do transfer\n'
                                  '4. Close account\n'
                                  '5. Log out\n'
                                  '0. Exit')
                            user_input_account = input()
                    else:
                        print('Such a card does not exist.\n'
                              '\n'
                              '1. Balance\n'
                              '2. Add income\n'
                              '3. Do transfer\n'
                              '4. Close account\n'
                              '5. Log out\n'
                              '0. Exit')
                        user_input_account = input()
                else:
                    print('Probably you made a mistake in the card number. Please try again!'
                          '\n'
                          '1. Balance\n'
                          '2. Add income\n'
                          '3. Do transfer\n'
                          '4. Close account\n'
                          '5. Log out\n'
                          '0. Exit')
                    user_input_account = input()
            if user_input_account == '4':
                db_delete_account(user_account, user_pin)
                print('The account has been closed!')
                break
            if user_input_account == '5':
                break
            if user_input_account == '0':
                user_input = '0'
                break
    else:
        print('Wrong card number or PIN!')


def db_connect():
    if path.exists("card.s3db"):
        conn = sqlite3.connect('card.s3db')
    else:
        conn = sqlite3.connect('card.s3db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE card ('
                    'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                    'number TEXT, '
                    'pin TEXT, '
                    'balance INTEGER DEFAULT 0);')
        conn.commit()


def db_add(generated_account, generated_pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("INSERT INTO card (number,pin) VALUES (?,?)", (generated_account, generated_pin))
    conn.commit()


def db_account_auth(generated_account, generated_pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM card WHERE number=? AND pin=?", (generated_account, generated_pin))
    result = cur.fetchone()
    return result[0]


def db_balance_query(generated_account, generated_pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("SELECT balance FROM card WHERE number=? AND pin=?", (generated_account, generated_pin))
    result = cur.fetchone()
    return result[0]


def db_delete_account(generated_account, generated_pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("DELETE FROM card WHERE number=? AND pin=?", (generated_account, generated_pin))
    conn.commit()


def db_add_income(generated_account, income):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("UPDATE card SET balance = balance + ? WHERE number=?", (income, generated_account,))
    conn.commit()


def db_deduct_balance(generated_account, sum):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("UPDATE card SET balance = balance - ? WHERE number=?", (sum, generated_account,))
    conn.commit()


def db_check_account(generated_account):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM card WHERE number=?", (generated_account,))
    result = cur.fetchone()
    return result[0]


print('1. Create an account\n'
      '2. Log into account\n'
      '0. Exit')
db_connect()
bank_accounts = dict()
bank_balance = dict()
user_input = input()
while user_input != '0':
    if user_input == '1':
        create_account()
    if user_input == '2':
        log_into_account()
        if user_input == '0':
            break
    print('\n'
          '1. Create an account\n'
          '2. Log into account\n'
          '0. Exit')
    user_input = input()
