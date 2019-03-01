#include <cs50.h>
#include <stdio.h>

// function placeholder
int get_height(string prompt);

int main(void)
{
    int height = get_height("Height: ");
    for (int hashs = 0; hashs < height; hashs++)
    {
        for (int spaces = 0; spaces < height - 1 - hashs ; spaces++)
        {
            printf(" ");
        }
        for (int line = 0; line < hashs + 1 ; line++)
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
    while (input < 1 || input > 8);
    return input;
}
