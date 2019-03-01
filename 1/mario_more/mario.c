#include <cs50.h>
#include <stdio.h>

// function placeholder
int get_height(string prompt);

int main(void)
{
    int height = get_height("Height: ");
    for (int counter = 0; counter < height; counter++)
    {
        for (int spaces = 0; spaces < height - 1 - counter ; spaces++)
            // print right whitespaces
        {
            printf(" ");
        }
        
        for (int hashs = 0; hashs < counter + 1 ; hashs++)
            // print right hashs
        {
            printf("#");
        }
        // print mid whitespace
        printf("  ");
        for (int hashs = 0; hashs < counter + 1 ; hashs++)
            // print left hashs
        {
            printf("#");
        }
        printf("\n");
    }
}

int get_height(string prompt)
// input must be a positive intger less than 8
{
    int input;
    do
    {
        input = get_int("%s", prompt);
    }
    // only accept the input if it's between 1 and 8
    while (input < 1 || input > 8);
    return input;
}
