from mmsimu import log
from mmsimu.allocation import Allocation
from mmsimu.types.integer import IntType
from mmsimu.types.character import CharType
from mmsimu.with_caller_info import with_caller_info


class MemoryManager:
    def __init__(self, heap_size, base_brk=0x0000_55D9_0000_0000):
        """
        heap_size: Maximum heap size in bytes. If the result of an
                   allocation would make the total allocated bytes
                   exceed this value, the allocation will fail.
        base_brk: Base address for allocated memory. This value is just
                  so that the simulated application can print pointers that
                  look "real". Any value can be used as it's not really
                  relevant to the simulation.
        """
        self.currently_allocated = 0
        self.allocations = []
        self.heap_size = heap_size
        self.brk = base_brk

    def malloc(self, size, caller):
        log.alloc(f"[{caller}] Requested {size} bytes")
        if self.currently_allocated + size > self.heap_size:
            log.alloc(
                f"[{caller}] Not enough memory (in use: {self.currently_allocated}, heap size: {self.heap_size})"
            )
            return Allocation(caller, 0, 0, None)

        allocation = Allocation(caller, size, address=self.brk)
        self.allocations.append(allocation)
        self.brk += size
        self.currently_allocated += size
        return allocation

    def realloc(self, allocation, size, caller):
        old_allocation = allocation.into_allocation()
        log.alloc(
            f"[{caller}] Reallocating block of size {old_allocation.size} to {size} bytes"
        )

        # We'll always move the memory somewhere else to prevent bugs of reusing
        # the old allocation / not checking realloc results.
        new_allocation = Allocation(
            caller, size, address=self.brk, old_contents=old_allocation.bytes[:]
        )
        self.free(old_allocation, caller)
        self.allocations.append(new_allocation)
        self.brk += size
        self.currently_allocated += size
        return new_allocation

    def free(self, obj, caller):
        allocation = obj.into_allocation()
        allocation.mark_freed()
        self.currently_allocated -= allocation.size
        self.allocations.remove(allocation)
        log.alloc(f"[{caller}] Freed {allocation.size} bytes")

    def sizeof(self, object):
        return object.sizeof()

    def print_leak_summary(self):
        leak_sources = {}
        total_leaked = 0
        for allocation in self.allocations:
            if leaks := leak_sources.get(allocation.allocated_at):
                leaks.append(allocation)
            else:
                leak_sources[allocation.allocated_at] = [allocation]

            total_leaked += allocation.size

        if leak_sources:
            print()
            print()
            print("======= MEMORY LEAKS FOUND!!! =======")
            for source, leaks in leak_sources.items():
                bytes_leaked = sum(leak.size for leak in leaks)
                print(
                    f"{bytes_leaked} bytes lost in {len(leaks)} allocations at {source}"
                )

            print("=====================================")
            print(
                f"Total lost: {total_leaked} bytes in {len(self.allocations)} allocations"
            )

    def __enter__(self):
        return self

    def __exit__(self, _, __, ___):
        self.print_leak_summary()
