#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    // Initialize variables
    float input;
    int cents;
    float quarter = 25;
    float dime = 10;
    float nickel = 5;
    float penny = 1;
    int counter = 0;
    // Prompt user for change input
    do
    {
        // Make sure input is more than zero
        input = get_float("Change owed: ");
        cents = round(input * 100);
    }
    while (input < 0);
    
    // Calcaulate the number of coins
    while (cents >= quarter)
    {
        cents = cents - quarter;
        counter++;
    }
    while (cents >= dime)
    {
        cents = cents - dime;
        counter++;
    }
    while (cents >= nickel) 
    {
        cents = cents - nickel;
        counter++;
    }
    while (cents >= penny)
    {
        cents = cents - penny;
        counter++;
    }
    // Print the output
    printf("%i\n", counter);
}
