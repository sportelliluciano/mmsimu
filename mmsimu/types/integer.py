import struct

from mmsimu.allocation import Allocation
from mmsimu.value import Value


class IntType:
    FORMAT = "<I"

    def sizeof(*_):
        return struct.calcsize(IntType.FORMAT)

    def to_str(allocation: Allocation):
        return str(IntType.to_native(allocation))

    def to_native(data: bytes) -> int:
        return struct.unpack(IntType.FORMAT, data)[0]

    def from_native(value: int) -> bytes:
        return struct.pack(IntType.FORMAT, value)

    def __call__(_, allocation):
        return Value(IntType, allocation)
