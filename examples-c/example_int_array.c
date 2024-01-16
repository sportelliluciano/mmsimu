#include <stdlib.h>
#include <stdio.h>

int main() {
    printf("Size of int array is: %d\n", sizeof(int) * 10);

    // Alloc space for array
    void *allocation = malloc(sizeof(int) * 10);
    printf("Memory address of allocated memory: %p\n", allocation);

    // Cast it to int* so we can use it
    // Reading a single integer and an array of integers is the same thing:
    //  `*int` is equivalent to `int[0]` and to `(int + 0*)`
    int* int_array = (int*)(allocation);

    // Printing the int* ends up in the same as printing the raw allocation
    // -- it prints the memory address
    printf("Memory address of allocated memory through int pointer: %p\n", int_array);

    printf("Writing 10, 20, 30, ..., 90 to each position of the array\n");
    // Let's write some values
    for (int i=0; i<10; i++) {
        // Note that we don't need `*` when indexing. This is also known as implicit deref.
        int_array[i] = i * 10;
    }

    printf("First element using *int_array: %d\n", *int_array);
    printf("First element using int_array[0]: %d\n", int_array[0]);
    printf("Third element using int_array[2]: %d\n", int_array[2]);

    // Note that pointer arithmetic automatically takes size in consideration:
    // Since int_array is of type int*, we know that:
    //   - The first integer (at index 0) will be at int_array base address + 0 bytes
    //   - The second will be at int_array base address + 8 bytes
    //   - The third at int_array base address + 16 bytes
    //   - ...and so on
    printf(
        "Third element using pointer arithmetic *(int_array + 2): %d\n",
        *(int_array + 2)
    );

    printf("Memory address of the first element: %p\n", (int_array + 0));
    printf("Memory address of the third element: %p\n", (int_array + 2));

    // Our int_array is just a pointer. That means it doesn't know how large our array is.
    // So we could access int_array[11]... but that leads to undefined behavior.
    // Depending on where is int_array stored, and how the underlying architecture handles
    // memory, several things could happen:
    //  - You may be reading (or writing) memory from a different variable
    //  - You may be reading (or writing) memory that belongs to your program but it's not
    //    been claimed by any variable yet.
    //  - You may be reading (or writing) memory where your program's own code is stored
    //  - The CPU/OS may detect that the read (or write) is invalid and crash your program
    //    with a Segmentation Fault error.
    //
    //
    // Note that calculating the address of the non-existing 11th element is not a problem:
    printf("Address of the non-existing 11th element: %p\n", int_array + 10);

    // Trying to dereference the element (either for reading or writing) in this language will 
    // generate undefined behavior. You can't tell what will happen.
    //
    // Uncomment the following lines to trigger it.
    //
    // int_array[10] = 123;
    // printf("Value of 11th element: %d\n", int_array[10]);

    // Note that since we requested a single block of memory for all integers,
    // we must free it as a block. We cannot free individual integers from the
    // block.
    free(int_array);
    return 0;
}