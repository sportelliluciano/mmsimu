import random

from mmsimu import log


class Allocation:
    def __init__(self, allocated_at, size, address=0, old_contents=None):
        """
        allocated_at: Information about the function that triggered this allocation
        size: Number of bytes to allocate
        address: Irrelevant, used just to print a pointer for the simulation
        old_contents: If reallocating, contents of the old allocation.
        """
        self.allocated_at = allocated_at
        self.address = address
        self.bytes = old_contents or []
        self.freed = False
        self.resize(size)

    @property
    def size(self):
        return len(self.bytes)

    def mark_freed(self):
        self.freed = True

    def resize(self, new_size):
        if self.size > new_size:
            self.bytes = self.bytes[:new_size]
        elif self.size < new_size:
            # None = uninitialized
            self.bytes = self.bytes + [None for _ in range(self.size, new_size)]

    def read(self, n_bytes, offset=0):
        assert (
            not self.freed
        ), f"Segmentation fault -- read after free {self.allocated_at}"
        assert (
            self != NULL
        ), f"Trying to read NULL pointer from failed allocation at {self.allocated_at}"

        if not (0 < offset + n_bytes <= self.size):
            raise Exception(
                f"Segmentation fault -- reading at base+{offset}, alloc size={self.size}, requested={n_bytes}"
            )

        warning_sent = False
        for i in range(offset, offset + n_bytes):
            if self.bytes[i] is None:
                if not warning_sent:
                    warning_sent = True
                    log.uninit("[WARNING] Reading uninitialized memory")

                self.bytes[i] = random.randint(0, 255)

        return bytes(self.bytes[offset : offset + n_bytes])

    def write(self, value, offset=0):
        assert (
            not self.freed
        ), f"Segmentation fault -- read after free {self.allocated_at}"
        assert (
            self != NULL
        ), f"Trying to write NULL pointer from failed allocation at {self.allocated_at}"

        if not (0 < offset + len(value) <= self.size):
            raise Exception(
                f"Segmentation fault -- writing at base+{offset}, alloc size={self.size}, requested={len(value)}"
            )

        for i, byte in enumerate(value):
            self.bytes[offset + i] = byte

    def into_allocation(self):
        return self

    @property
    def deref(self):
        raise Exception("Can't dereference raw memory -- cast it to a type first")

    @deref.setter
    def deref(self, _):
        raise Exception("Can't dereference raw memory -- cast it to a type first")

    def __str__(self):
        return f"0x{self.address:x}"

    def __int__(self):
        return self.address

    def __eq__(self, other):
        return int(self) == int(other)


NULL = 0
