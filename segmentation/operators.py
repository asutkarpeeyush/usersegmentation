import operator
from collections import Callable


class Operator:
    def __init__(self, name: str, operation: Callable):
        self.name = name
        self.operation = operation


class KeyOperator(Operator):
    def __init__(self, name: str, operation: Callable):
        if operation not in [operator.or_, operator.and_]:
            raise Exception("Only or/and operators can be of type KeyOperator")
        super(KeyOperator, self).__init__(name, operation)
