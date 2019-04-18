#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    // Make sure that command-line arguments are one
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // Open RAW file
    FILE *file = fopen(argv[1], "r");

    // Make sure that file exists
    if (file == NULL)
    {
        fprintf(stderr, "File %s is not found.\n", argv[1]);
        return 2;
    }

    // Create output file
    FILE *img = NULL;

    // Create buffer and filename arrays
    unsigned char buffer[512];
    char filename[8];

    // Set counter for filename
    int counter = 0;

    // Set flag for JPEG
    bool flag = false;

    // Read RAW file
    while (fread(buffer, 512, 1, file) == 1)
    {
        // Check if we are at the beginning of a JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close current JPEG, so we can start reading the next
            if (flag == true)
            {
                fclose(img);
            }
            // Condition for found JPEG
            else
            {
                flag = true;
            }

            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "w");
            counter++;
        }

        if (flag == true)
        {
            // Write image contents
            fwrite(&buffer, 512, 1, img);
        }
    }

    // Close all files
    fclose(file);
    fclose(img);

    // Success
    return 0;
}
