from mmsimu.all import *

# Example of heap exhaustion


def main():
    # The default heap size for this simulator is 1024 bytes.
    # There's a caveat, though: the simulator will keep track of how much
    # memory was allocated, but will not actually allocate memory from a heap
    # and will use the system heap instead. This means that we can always make
    # use of the full 1024 bytes because there is no possibility for memory
    # fragmentation.

    # Trying to allocate more memory than what we have available will fail
    allocation = malloc(2000)
    printf("malloc(%d) returned: %p\n", 2000, allocation)

    # malloc inform us that it failed by returning the special memory address 0x0.
    # There's an alias defined for that special address: NULL
    # Robust code will always check if malloc returned NULL before using the newly
    # allocated memory.
    assert allocation == NULL

    # If we allocate integers separately, we'll be able to allocate until
    # we exhaust our 1024 bytes heap. Since each integer is 4 bytes long,
    # we'll be able to allocate only 256 integers until we run out of memory.
    allocations = []
    while True:
        allocation = malloc(sizeof(int32_t))
        if allocation == NULL:
            printf("malloc failed after allocating %d ints!!\n", len(allocations))
            break

        # Note that we are using a bit of classic Python here!
        allocations.append(allocation)

    # At this point our heap is exhausted because of all the ints we have in
    # the allocations array.
    #
    # Any new allocation will fail until we free a bit of that memory
    allocation = malloc(1)
    printf("malloc(1) returned: %p\n", allocation)
    assert allocation == NULL

    # If we free an int...
    some_int = allocations.pop()
    printf("Freeing int32_t at %p\n", some_int)
    free(some_int)

    # ...we should now be able to malloc up to 4 bytes more!
    two_bytes = malloc(2)
    printf("malloc(2) returned: %p\n", two_bytes)
    assert two_bytes != NULL
    free(two_bytes)

    # You should free the memory afterwards, otherwise you'll get a leak summary
    # when the program finishes
    for int in allocations:
        free(int)


mmsimu_init(main)
