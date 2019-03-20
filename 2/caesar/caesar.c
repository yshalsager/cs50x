#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void prompt_and_exit();

int main(int argc, string argv[])
{
    // Ensure that command line argument is one and digit
    if (argc != 2)
    {
        prompt_and_exit();
    }
    // Ensure that command line argument is number
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            prompt_and_exit();
        }
    }
    // Convert argv[1] to intger
    int key = atoi(argv[1]);
    // Ensure that command line argument is postive number
    if (key < 0)
    {
        prompt_and_exit();
    }
    // Ask user for the input
    string text = get_string("plaintext: ");
    // Iterate over every character in the plaintext and encrypt
    printf("ciphertext: ");
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isupper(text[i]))
        {
            printf("%c", 'A' + (text[i] - 'A' + key) % 26);
        }
        else if (islower(text[i]))
        {
            printf("%c", 'a' + (text[i] - 'a' + key) % 26);
        }
        else
        {
            printf("%c", text[i]);
        }
    }
    printf("\n");
    return 0;
}

void prompt_and_exit()
{
    // Prompt the user continusally for the usage
    printf("Usage: ./caesar key\n");
    exit(1);
}
