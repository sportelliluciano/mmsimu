import inspect


def with_caller_info(fn):
    """
    Adds the function name and line number of the caller function
    as the last parameter to the function being called.

    Example:

    def test_func():
        f2(37)

    @with_caller_info
    def f2(number, caller):
        print(f"Called from {caller} with number = {number}")

    test_func()  # will print 'Called from [test_func:2] with number = 37'
    """

    def decorated(*args, **kwargs):
        # Returns current frame, caller's frame, [caller's frame^2, caller's frame^3, ...]
        _, caller_frame, *_ = inspect.getouterframes(inspect.currentframe(), 2)
        caller_info = f"{caller_frame.function}:{caller_frame.lineno}"
        kwargs["caller"] = caller_info
        return fn(
            *args,
            **kwargs,
        )

    return decorated
