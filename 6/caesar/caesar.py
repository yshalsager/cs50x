#!/usr/bin/env python3
# caesar

from sys import argv
from cs50 import get_string


def prompt_and_exit():
    # Prompt the user for the usage
    print('Usage: python caesar.py k')
    exit(1)


def check_key():
    # Ensure that command line argument is a digit
    if not argv[1].isdigit():
        prompt_and_exit()
    # Convert argv[1] to integer
    key = int(argv[1])
    if key < 0:  # Ensure that command line argument is positive number
        prompt_and_exit()
    return key


def main():
    # Ensure that command line argument is one
    if len(argv) != 2:
        prompt_and_exit()
    key = check_key()
    # Ask user for the input
    text = get_string("plaintext: ")
    print("ciphertext: ", end='')
    for c in text:  # Iterate over every character in the plaintext and encrypt
        if c.isupper():
            print(chr(ord('A') + (ord(c) - ord('A') + key) % 26), end='')
        elif c.islower():
            print(chr(ord('a') + (ord(c) - ord('a') + key) % 26), end='')
        else:
            print(c, end='')
    print()
    return 0


if __name__ == '__main__':
    main()
