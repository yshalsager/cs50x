#!/usr/bin/env python3
# Mario less

from cs50 import get_int


def get_height():
    while True:
        height = get_int("Height: ")
        if 0 < height <= 8:
            return height


def main():
    height = get_height()
    for hashs in range(height):
        for spaces in range(height - 1 - hashs):
            # print right whitespaces
            print(' ', end='')
        for line in range(hashs + 1):
            # print right hashs
            print('#', end='')
        print('\n', end='')


if __name__ == '__main__':
    main()
