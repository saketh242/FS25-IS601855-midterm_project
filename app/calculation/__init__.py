from abc import ABC, abstractmethod
import string

from app.operations import Operations

class Calculation(ABC):

    def __init__(self, a: float, b: float) -> None:

        self.a: float = a
        self.b: float = b
    
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
            return AddCalculation(a, b)
        elif calculation_type == "subtract":
            return SubtractCalculation(a,b)
        elif calculation_type == "mulitply":
            return MultiplyCalculation(a, b)
        elif calculation_type == "divide":
            return DivideCalculation(a, b)
        

class AddCalculation(Calculation):

    def __init__(self, a:float, b:float) -> None:
        self.a: float = a
        self.b: float = b
    
    def execute(self) -> float:
        return Operations.add(self.a, self.b)

    def __str__(self):
        return f"{self.a} + {self.b} = {self.execute()}"

class SubtractCalculation(Calculation):
    def __init__(self, a:float, b:float) -> None:
        self.a: float = a
        self.b: float = b
    
    def execute(self) -> float:
        return Operations.subtract(self.a, self.b)

    def __str__(self):
        return f"{self.a} - {self.b} = {self.execute()}"

class MultiplyCalculation(Calculation):
    def __init__(self, a:float, b:float) -> None:
        self.a: float = a
        self.b: float = b
    
    def execute(self) -> float:
        return Operations.multiply(self.a, self.b)

    def __str__(self):
        return f"{self.a} * {self.b} = {self.execute()}"

class DivideCalculation(Calculation):
    def __init__(self, a:float, b:float) -> None:
        self.a: float = a
        self.b: float = b
    
    def execute(self) -> float:
        return Operations.divide(self.a, self.b)

    def __str__(self):
        return f"{self.a} / {self.b} = {self.execute()}"



