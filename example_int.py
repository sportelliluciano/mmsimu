from mmsimu.all import *

# Alloc memory for a single integer


def main():
    printf("Size of int is: %d\n", sizeof(int32_t))

    # Alloc space for an int32
    # Allocation may fail, in that case it returns None
    allocation = malloc(sizeof(int32_t))
    printf("Memory address of allocated memory: %p\n", allocation)

    # Cast it to int32* so we can use it
    an_int = (int32_ptr_t)(allocation)

    # Printing the int* ends up in the same as printing the raw allocation
    # -- it prints the memory address
    printf("Memory address of allocated memory through int pointer: %p\n", an_int)

    # If we want the value we need to de-reference it
    # The following line will print a random number because this memory is not initialized
    printf("Value of uninitialized memory: %d\n", an_int.deref)

    # If we want to write a new value we also need to de-reference first
    an_int.deref = 11

    # Prints 11
    printf("Value of memory after writing `11` to it: %d\n", an_int.deref)

    # You should free the memory afterwards, otherwise you'll get a leak summary
    # when the program finishes
    free(an_int)


mmsimu_init(main)
