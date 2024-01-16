class Value:
    """
    Value with an associated type.

    This class holds all of the syntactic sugar to dereference pointer
    values.
    """

    def __init__(self, type, allocation, base_offset=0):
        self.type = type
        self.base_offset = base_offset
        self.allocation = allocation
        

    @property
    def deref(self):
        return self[0]

    @deref.setter
    def deref(self, new_native_value):
        self[0] = new_native_value

    def __setitem__(self, index, value):
        offset = self.base_offset + self.type.sizeof() * index
        self.allocation.write(self.type.from_native(value), offset=offset)

    def __getitem__(self, index):
        offset = self.base_offset + self.type.sizeof() * index
        data = self.allocation.read(self.type.sizeof(), offset=offset)
        return self.type.to_native(data)

    def __add__(self, integer):
        return Value(
            self.type, self.allocation, base_offset=(integer * self.type.sizeof())
        )

    def __int__(self):
        return self.allocation.address + self.base_offset

    def __str__(self):
        return f"0x{self.allocation.address + self.base_offset:x}"

    def into_allocation(self):
        if self.base_offset != 0:
            raise Exception(
                "This pointer does not point to the `start` of an allocation"
            )
        return self.allocation
