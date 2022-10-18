from typing import (
    NewType,
)

one = NewType("dims=1", int)
two = NewType("dims=2", int)
three = NewType("dims=3", int)
four = NewType("dims=4", int)
five = NewType("dims=5", int)
six = NewType("dims=6", int)
N = NewType("dims=N", int)
# __builtins__.__getitem__ = None
