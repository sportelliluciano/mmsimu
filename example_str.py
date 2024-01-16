from mmsimu.all import *

# Realloc & basic string operations
#   - realloc
#   - str_len
#   - string iteration
#   - string shortening, offseting, enlarging


def main():
    printf("Size of char is: %d\n", sizeof(char_t))

    # Strings are just arrays of characters with an invariant:
    #  The last character is always a null terminator '\0'.
    #
    # So for the string "hello", in memory it would require 6 characters:
    #     'h' 'e' 'l' 'l' 'o' '\0'
    #
    # We'll allocate 6 characters for our string
    allocation = malloc(sizeof(char_t) * 6)
    printf("Memory address of allocated memory: %p\n", allocation)

    # Let's cast it to char* so we can use it
    my_str = (char_ptr_t)(allocation)

    # Similar to how int arrays work, if we deref our pointer we'll be writing
    # to the first character of the string
    #
    # Note that a character is just a number. There is table that tells you which
    # number is assigned to each character. You can look it up in Internet, it's
    # called the ASCII table. For example, 'h' is assigned number 104.
    #
    # Also note that 'h' and 'H' are assigned different numbers. Otherwise the
    # computer wouldn't be able to tell them apart!.
    my_str.deref = "h"

    # Trying to print the string using `deref` will only print the first character!
    # No special treatment for strings -- remember it's just an array of numbers.
    printf("Reading first character of the string: %c\n", my_str.deref)

    # We can write the rest of the string just as we did for the integer array:
    for i, character in enumerate("hello"):
        my_str[i] = character

    # And don't forget the null terminator at the end!
    my_str[len("hello")] = 0

    # Again, no special treatment for strings, if we want to print it out, we need
    # to loop the character array. Let's write a function to do so.
    printf("The string is: '%s'\n", my_str)

    # If we want to know the size of the string, we need to calculate it:
    printf("The len of the string is: %d\n", str_len(my_str))

    # If we want to enlarge our string, we'll need to allocate more memory.
    #
    # We have options here:
    #  - We could malloc a bigger block of memory, then copy our string there
    #    and then free our old block of memory.
    #  - Or we can use realloc.
    #
    # The realloc function will try to increase the size of our old block of
    # memory without copying it. Sometimes this is possible and the operation
    # is very cheap. Sometimes is not and realloc is just as expensive as
    # allocating a new block of memory then copying the contents and freeing
    # the old block.
    #
    # There's a caveat: if realloc fails because the system is out of memory,
    # it will do nothing and return None instead. So we should take care of
    # that case separately.
    #
    # Let's extend our string to "hello world"
    new_str = realloc(
        my_str, sizeof(char_t) * (len("hello world") + 1)
    )  # Don't forget \0
    if not new_str:
        # Realloc failed!
        # We'll need to free our old block and just exit the program: the system is out of memory
        printf("System is out of memory!\n")
        free(my_str)  # Not freeing my_str will result in a memory leak
        return

    # If we reached this point, realloc succeded. This means that:
    #  - my_str was automatically freed by realloc
    #  - new_str contains the new, bigger block. Similar to malloc, realloc also
    #    returns "raw memory", so let's cast it to char* and reuse the old name my_str
    my_str = (char_ptr_t)(new_str)

    # We can now copy the rest of our string. We already had "hello" in there so
    # we'll add " world" after it.
    for i, character in enumerate(" world"):
        my_str[len("hello") + i] = character

    # Null terminator :)
    my_str[len("hello world")] = 0

    # Let's print the result!
    printf(f"Extended string: '%s'\n", my_str)

    # Now, since our string is just a pointer to an array of characters, we can make use of
    # some pointer arithemtic to write just the last part of a string, for example, if we
    # start reading my_str from the 6th character
    printf(f"String offset by 6 characters: '%s'\n", my_str + 6)

    # Shortening strings is much easier: we only need to move the null terminator.
    # For example, we could shorten "hello world" to "he" by putting the null
    # terminator in the third position:
    my_str[2] = 0
    printf(f"Shortened string: '%s'\n", my_str)

    # Note that shortening the string does not free the allocated memory. It's just
    # there not being used.

    # You should free the memory afterwards, otherwise you'll get a leak summary
    # when the program finishes
    free(my_str)


def str_len(s):
    # We want to count how many characters a string has.
    #
    # But there's a catch: The only thing we know is the memory address of the
    # first character. How do we tell where the string ends?
    #
    # Well, we know the string must hold an invariant that we mentioned earlier:
    #   - The last character in a string is always a null terminator '\0'
    i = 0
    while s[i] != "\0":
        i += 1

    return i


mmsimu_init(main)
