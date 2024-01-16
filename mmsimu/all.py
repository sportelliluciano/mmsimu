import mmsimu.types.integer
import mmsimu.types.character

from mmsimu.main import mmsimu_init
from mmsimu.allocation import NULL
from mmsimu.instance import get_instance
from mmsimu.with_caller_info import with_caller_info

int32_t = mmsimu.types.integer.IntType()
int32_ptr_t = mmsimu.types.integer.IntType()
char_t = mmsimu.types.character.CharType()
char_ptr_t = mmsimu.types.character.CharType()



@with_caller_info
def malloc(size, caller):
    return get_instance().malloc(size, caller)


@with_caller_info
def realloc(ptr, size, caller):
    return get_instance().realloc(ptr, size, caller)


@with_caller_info
def free(ptr, caller):
    return get_instance().free(ptr, caller)


def sizeof(type):
    return get_instance().sizeof(type)


def printf(format, *args):
    # Reduced implementation of printf for demo purposes
    in_format = False

    current_arg = 0
    result = ""
    for c in format:
        if in_format:
            if c == "%":
                result += "%"
            elif c in ("p", "d", "i"):
                value = int(args[current_arg])
                if c == "p":
                    result += f"0x{value:x}"
                else:
                    result += str(value)
                current_arg += 1
            elif c == "s":
                result += to_python_string(args[current_arg])
                current_arg += 1
            elif c == "c":
                result += args[current_arg]
                current_arg += 1
            else:
                raise Exception(f"Unrecognized format in printf: `%{c}`")
            in_format = False
        else:
            if c == "%":
                in_format = True
            else:
                result += c

    if current_arg != len(args):
        raise Exception(f"Unused format arguments: {args[current_arg:]}")

    print(result, end="")


def to_python_string(s):
    result = ""
    i = 0
    while s[i] != "\0":
        result += s[i]
        i += 1

    return result
