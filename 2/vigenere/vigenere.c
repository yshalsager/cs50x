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
    // Ensure that command line argument is word
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isalpha(argv[1][i]))
        {
            printf("You've entered non-alphabetical characters.\n"); 
            prompt_and_exit();
        }
    }
    string key = argv[1];
    int key_len = strlen(key);
    // Ask user for the input
    string text = get_string("plaintext: ");
    // Iterate over every character in the plaintext and encrypt
    printf("ciphertext: ");
    int n = strlen(text);
    int counter = 0;
    int j;
    int k;
    for (int i = 0; i < n; i++)
    {
        j = (counter % key_len);
        // Encrypt uppercase
        if (isupper(text[i]))
        {
            k = (tolower(key[j]) - 97);
            printf("%c", (((text[i] + k) - 'A') % 26) + 'A');
            counter++;
        }
        // Encrypt lowercase
        else if (islower(text[i]))
        {
            k = (tolower(key[j]) - 97);
            printf("%c", (((text[i] + k) - 'a') % 26) + 'a');
            counter++;
        }
        // Skip
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
    printf("Usage: ./vigenere keyword\n");
    exit(1);
}
