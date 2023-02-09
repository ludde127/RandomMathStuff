

def _is_variable_same_name(method):
    def inner(_self, other):
        if Variable.matching_other_variable(_self, other):
            return method(_self, other)
        raise TypeError("Both are not variables with the same name.")

    return inner


class Variable:
    def __init__(self, name: str, coefficient: float = 1, power: float = 1):
        self.coefficient = coefficient
        self.name = name
        self.power = power

    @_is_variable_same_name
    def __add__(self, other):
        if other.power == self.power:
            return Variable(name=self.name, coefficient=self.coefficient + other.coefficient, power=self.power)
        raise TypeError()

    @_is_variable_same_name
    def __sub__(self, other):
        if other.power == self.power:
            return Variable(name=self.name, coefficient=self.coefficient - other.coefficient, power=self.power)
        raise TypeError()

    @_is_variable_same_name
    def __mul__(self, other):
        return Variable(name=self.name, coefficient=self.coefficient * other.coefficient, power=self.power + other.power)

    @_is_variable_same_name
    def __truediv__(self, other):
        return Variable(name=self.name, coefficient=self.coefficient / other.coefficient, power=self.power - other.power)

    def __hash__(self):
        return f"{self.name}, power {self.power}".__hash__()

    def __str__(self):
        return f"{self.coefficient}*({self.name}^{self.power})"

    def __repr__(self):
        return str(self)

    @staticmethod
    def matching_other_variable(first, other):
        return isinstance(first, Variable) and isinstance(other, Variable) and first.name == other.name


def _other_is_variable(method):
    def inner(_self, other):
        if isinstance(other, Variable):
            return method(_self, other)
        raise TypeError(f"Other should be variable not {type(other)}.")

    return inner


class Polynomial:
    def __init__(self):
        self.parts = dict()
        self.multiplier = None
        self.divisor = None

    def get_variable_same_pow(self, variable: Variable):
        return self.parts.get(variable, None)

    @_other_is_variable
    def __add__(self, other):
        if existing := self.get_variable_same_pow(other):
            self.parts[other] = existing + other
        else:
            self.parts[other] = other
        return self

    @_other_is_variable
    def __sub__(self, other):
        if existing := self.get_variable_same_pow(other):
            self.parts[other] = existing - other
        else:
            self.parts[other] = other
        return self

    @_other_is_variable
    def __mul__(self, other):
        if self.multiplier is None:
            self.multiplier = Polynomial()
        self.multiplier = self.multiplier + other
        return self

    @_other_is_variable
    def __div__(self, other):
        if self.divisor is None:
            self.divisor = Polynomial()
        self.divisor = self.divisor + other
        return self

    def __repr__(self):
        return str(self)

    def __str__(self):
        main = "(" + " + ".join([str(v) for v in self.parts.values()]) + ")"
        if self.multiplier is not None and self.multiplier.parts:
            main = str(self.multiplier) + " * " + main
        if self.divisor is not None and self.divisor.parts:
            main = main + " / " + str(self.divisor)
        return main
