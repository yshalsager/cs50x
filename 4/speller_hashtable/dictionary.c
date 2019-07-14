// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Counter for the words in size function
int word_count = 0;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        fprintf(stderr, "Could not open file %s.\n", dictionary);
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];
    int n = LENGTH + 2;

    // Loop through the dictionary until a null character
    while (fgets(word, n, file) != NULL)
    {
        // Add null terminator to the end of the word
        word[strlen(word) - 1] = '\0';
        // Hash the word
        int index = hash(word) % N;
        // Create a temporary node
        node *temp = malloc(sizeof(node));
        // Test to see if node is null
        if (temp == NULL)
        {
            fclose(file);
            return false;
        }
        // Move to the next node in the list
        strcpy(temp -> word, word);
        temp -> next = hashtable[index];
        hashtable[index] = temp;
        word_count++;
    }

    // Close dictionary
    fclose(file);
    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Convert word to lowercase
    int n = strlen(word);
    char copy[n + 1];
    // Add null terminator to end of the lower case word
    copy[n] = '\0';

    for (int i = 0; i < n; i++)
    {
        copy[i] = tolower(word[i]);
    }
    // Pass lower case word to hash function to get index
    int index = hash(copy) % N;
    // Set to the head of the linked list
    node *head = hashtable[index];
    if (head != NULL)
    {
        // Points the cursor to the same location
        node *cursor = head;
        // Traverse the linked list
        while (cursor != NULL)
        {
            if (strcmp(copy, cursor->word) == 0)
            {
                // Return true if word matches the word in our dictionary
                return true;
            }
            // Else move cursor to the next linked list
            cursor = cursor->next;
        }
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // For each node in the hashtable
    for (int i = 0; i < N; i++)
    {
        // Check the table for a node at that index
        node *cursor = hashtable[i];
        while (cursor != NULL)
        {
            // Create a temporary node
            node *temp = cursor;
            cursor = cursor -> next;
            // Free the current node
            free(temp);
        }
    }
    return true;
}
