from cs50 import get_string
from sys import argv


def main():
    # Ensure that command line argument is one
    if len(argv) != 2:
        print('Usage: python bleep.py dictionary')
        exit(1)
    words = set()
    # load words from file
    with open(argv[1], 'r') as dictionary:
        for item in dictionary:
            words.add(item.strip())
    text = get_string("What message would you like to censor?\n")
    # censor the message
    censored = []
    for word in text.split(" "):
        if word.lower() in words:
            censor = ''.join(['*' for c in word])
            censored.append(censor)
        else:
            censored.append(word)
    print(' '.join(censored))


if __name__ == "__main__":
    main()
