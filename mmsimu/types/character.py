import struct

from mmsimu.allocation import Allocation
from mmsimu.value import Value


class CharType:
    FORMAT = "<c"

    def sizeof(*_):
        return struct.calcsize(CharType.FORMAT)

    def to_str(allocation: Allocation):
        return str(CharType.to_native(allocation))

    def to_native(data: bytes) -> str:
        assert len(data) == 1
        return data.decode("ascii")

    def from_native(value: str | int) -> bytes:
        if isinstance(value, str):
            assert len(value) == 1
            assert 0 <= ord(value) < 256
            return struct.pack(CharType.FORMAT, value.encode("ascii"))
        elif isinstance(value, int):
            assert 0 <= value < 256
            return struct.pack(CharType.FORMAT, bytes([value]))
        else:
            raise Exception("Type cannot be coerced to `char`")

    def __call__(_, allocation):
        return Value(CharType, allocation)
