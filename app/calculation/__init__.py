from abc import ABC, abstractmethod

from app.operations import Operations


class Calculation(ABC):

    def __init__(self, a: float, b: float, operation: str = "") -> None:

        self.a: float = a
        self.b: float = b
        self.operation: str = operation

    @abstractmethod
    def execute(self) -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class CalculationFactory:

    @staticmethod
    def register_calculation(calculation_type: str, a: float, b: float) -> Calculation:
        if calculation_type == "add":
            return AddCalculation(a, b, calculation_type)
        elif calculation_type == "subtract":
            return SubtractCalculation(a, b, calculation_type)
        elif calculation_type == "multiply":
            return MultiplyCalculation(a, b, calculation_type)
        elif calculation_type == "divide":
            return DivideCalculation(a, b, calculation_type)
        elif calculation_type == "power":
            return PowerCalculation(a, b, calculation_type)
        elif calculation_type == "root":
            return RootCalculation(a, b, calculation_type)
        elif calculation_type == "modulus":
            return ModulusCalculation(a, b, calculation_type)
        elif calculation_type == "absolute difference":
            return AbsoluteDifferenceCalculation(a, b, calculation_type)
        elif calculation_type == "integer division":
            return IntegerDivisionCalculation(a, b, calculation_type)
        elif calculation_type == "percentage":
            return PercentageCalculation(a, b, calculation_type)


class AddCalculation(Calculation):

    def __init__(self, a: float, b: float, operation: str = "") -> None:
        self.a: float = a
        self.b: float = b
        self.operation: str = operation

    def execute(self) -> float:
        return Operations.add(self.a, self.b)

    def __str__(self):
        return f"{self.a} + {self.b} = {self.execute()}"


class SubtractCalculation(Calculation):
    def __init__(self, a: float, b: float, operation: str = "") -> None:
        self.a: float = a
        self.b: float = b
        self.operation: str = operation

    def execute(self) -> float:
        return Operations.subtract(self.a, self.b)

    def __str__(self):
        return f"{self.a} - {self.b} = {self.execute()}"


class MultiplyCalculation(Calculation):
    def __init__(self, a: float, b: float, operation: str = "") -> None:
        self.a: float = a
        self.b: float = b
        self.operation: str = operation

    def execute(self) -> float:
        return Operations.multiply(self.a, self.b)

    def __str__(self):
        return f"{self.a} * {self.b} = {self.execute()}"


class DivideCalculation(Calculation):
    def __init__(self, a: float, b: float, operation: str = "") -> None:
        self.operation: str = operation
        self.a: float = a
        self.b: float = b
        self.operation: str = operation

    def execute(self) -> float:
        return Operations.divide(self.a, self.b)

    def __str__(self):
        return f"{self.a} / {self.b} = {self.execute()}"


class PowerCalculation(Calculation):
    def __init__(self, a: float, b: float, operation: str = "") -> None:
        self.a: float = a
        self.b: float = b
        self.operation: str = operation

    def execute(self) -> float:
        return Operations.power(self.a, self.b)

    def __str__(self):
        return f"{self.a} ^ {self.b} = {self.execute()}"


class RootCalculation(Calculation):
    def __init__(self, a: float, b: float, operation: str = "") -> None:
        self.a: float = a
        self.b: float = b
        self.operation: str = operation

    def execute(self) -> float:
        return Operations.root(self.a, self.b)

    def __str__(self):
        return f"{self.a} root {self.b} = {self.execute()}"

class ModulusCalculation(Calculation):
    def __init__(self, a: float, b: float, operation: str = "") -> None:
        self.a: float = a
        self.b: float = b
        self.operation: str = operation
    def execute(self) -> float:
        return Operations.modulus(self.a, self.b)

    def __str__(self):
        return f"{self.a} modulus {self.b} = {self.execute()}"

class IntegerDivisionCalculation(Calculation):
    def __init__(self, a: float, b: float, operation: str = "") -> None:
        self.a: float = a
        self.b: float = b
        self.operation: str = operation

    def execute(self) -> float:
        return Operations.integer_division(self.a, self.b)

    def __str__(self):
        return f"{self.a} integer division {self.b} = {self.execute()}"

class PercentageCalculation(Calculation):
    def __init__(self, a: float, b: float, operation: str = "") -> None:
        self.a: float = a
        self.b: float = b
        self.operation: str = operation

    def execute(self) -> float:
        return Operations.percentage(self.a, self.b)

    def __str__(self):
        return f"{self.a} % {self.b} = {self.execute()}"

class AbsoluteDifferenceCalculation(Calculation):
    def __init__(self, a: float, b: float, operation: str = "") -> None:
        self.a: float = a
        self.b: float = b
        self.operation: str = operation

    def execute(self) -> float:
        return Operations.absolute_difference(self.a, self.b)

    def __str__(self):
        return f"{self.a} absolute difference {self.b} = {self.execute()}"