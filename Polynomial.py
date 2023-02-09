class Variable:
    def __init__(self, name: str, coefficient: float = 1, power: float = 1):
        self.coeff = coefficient
        self.name = name
        self.power = power

    def __add__(self, other):
        if isinstance(other, Variable) and other.name == self.name and other.power == self.power:
            return Variable(name=self.name, coefficient=self.coeff + other.coeff, power=self.power)
        raise TypeError()

    def __sub__(self, other):
        if isinstance(other, Variable) and other.name == self.name and other.power == self.power:
            return Variable(name=self.name, coefficient=self.coeff - other.coeff, power=self.power)
        raise TypeError()

    def __mul__(self, other):
        if isinstance(other, Variable) and other.name == self.name:
            return Variable(name=self.name, coefficient=self.coeff * other.coeff, power=self.power+other.power)
        raise TypeError()

    def __truediv__(self, other):
        if isinstance(other, Variable) and other.name == self.name:
            return Variable(name=self.name, coefficient=self.coeff / other.coeff, power=self.power-other.power)
        raise TypeError()

    def __hash__(self):
        return f"{self.name}, power {self.power}".__hash__()

    def __str__(self):
        return f"{self.coeff}*({self.name}^{self.power})"

    def __repr__(self):
        return str(self)


class Polynomial:
    def __init__(self):
        self.parts = dict()
        self.multiplier = None
        self.divisor = None

    def get_variable_same_pow(self, variable: Variable):
        return self.parts.get(variable, None)

    def __add__(self, other):
        if isinstance(other, Variable):
            if existing := self.get_variable_same_pow(other):
                self.parts[other] = existing + other
            else:
                self.parts[other] = other
            return self
        raise TypeError()

    def __sub__(self, other):
        if isinstance(other, Variable):
            if existing := self.get_variable_same_pow(other):
                self.parts[other] = existing - other
            else:
                self.parts[other] = other
            return self
        raise TypeError()

    def __mul__(self, other):
        if isinstance(other, Variable):
            if self.multiplier is None:
                self.multiplier = Polynomial()
            self.multiplier = self.multiplier + other
            return self
        raise TypeError()

    def __div__(self, other):
        if isinstance(other, Variable):
            if self.divisor is None:
                self.divisor = Polynomial()
            self.divisor = self.divisor + other
            return self
        raise TypeError()

    def __repr__(self):
        return str(self)

    def __str__(self):
        main = "(" + " + ".join([str(v) for v in self.parts.values()]) + ")"
        if self.multiplier is not None and self.multiplier.parts:
            main = str(self.multiplier) + " * " + main
        if self.divisor is not None and self.divisor.parts:
            main = main + " / " + str(self.divisor)
        return main
