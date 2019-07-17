#!/usr/bin/env python3
# Cash

from cs50 import get_float


def get_change():
    # get the round value of input
    while True:
        change = get_float("Change owed: ")
        cents = round(change * 100)
        if change > 0:
            return cents


def main():
    cents = get_change()
    quarter = 25
    dime = 10
    nickel = 5
    penny = 1
    counter = 0
    # start looping and counting
    while cents >= quarter:
        cents = cents - quarter
        counter = counter + 1
    while cents >= dime:
        cents = cents - dime
        counter = counter + 1
    while cents >= nickel:
        cents = cents - nickel
        counter = counter + 1
    while cents >= penny:
        cents = cents - penny
        counter = counter + 1
    print(counter)


if __name__ == '__main__':
    main()

