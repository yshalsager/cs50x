// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

void prompt_and_exit();

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        prompt_and_exit();
    }

    // Convert argv[1] to intger
    int n = atoi(argv[1]);

    // Ensure that command line argument is postive number
    if (n < 0 || n > 180)
    {
        printf("Resize value must be a number between 0 and 100\n");
        prompt_and_exit();
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // Create variables for original width and height
    int originalWidth = bi.biWidth;
    int originalHeight = bi.biHeight;

    // Update width and height
    bi.biWidth *= n;
    bi.biHeight *= n;

    // Determine padding for scanlines
    int originalPadding = (4 - (originalWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // update image size
    bi.biSizeImage = abs(bi.biHeight) * ((bi.biWidth * sizeof(RGBTRIPLE)) + padding);

    // update file size
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // Allocate storage for buffer
    RGBTRIPLE *buffer = malloc(sizeof(RGBTRIPLE) * (bi.biWidth));

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(originalHeight); i < biHeight; i++)
    {
        int counter = 0;
        // iterate over pixels in scanline
        for (int j = 0; j < originalWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // write pixel to buffer n times
            for (int count = 0; count < n; count++)
            {
                *(buffer + (counter)) = triple;
                counter++;
            }
        }

        // skip over padding, if any
        fseek(inptr, originalPadding, SEEK_CUR);

        // write RGB triple to outfile
        for (int r = 0; r < n; r++)
        {
            fwrite((buffer), sizeof(RGBTRIPLE), bi.biWidth, outptr);

            // write padding to outfile
            for (int k = 0; k < padding; k++)
            {
                fputc(0x00, outptr);
            }
        }
    }

    // free memory from buffer
    free(buffer);

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);


    // success
    return 0;
}


void prompt_and_exit()
{
    // Prompt the user continusally for the usage
    printf("Usage: ./resize n infile outfile\n");
    exit(1);
}
