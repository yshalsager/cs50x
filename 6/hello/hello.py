#!/usr/bin/env python3
# Hello World

from cs50 import get_string


def main():
    name = get_string("What is your name? ")
    print(f'hello, {name}')


if __name__ == '__main__':
    main()
