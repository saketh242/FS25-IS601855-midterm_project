import os

class Operations:

    @staticmethod
    def _validate_input(value):
        max_value = float(os.getenv('CALCULATOR_MAX_INPUT_VALUE', '999999999'))
        if abs(value) > max_value:
            raise ValueError(f"Input value {value} exceeds maximum allowed value {max_value}")

    @staticmethod
    def add(a, b):
        Operations._validate_input(a)
        Operations._validate_input(b)
        return round(a + b, int(os.getenv('CALCULATOR_PRECISION')))

    @staticmethod
    def subtract(a, b):
        Operations._validate_input(a)
        Operations._validate_input(b)
        return round(a - b, int(os.getenv('CALCULATOR_PRECISION')))

    @staticmethod
    def multiply(a, b):
        Operations._validate_input(a)
        Operations._validate_input(b)
        return round(a * b, int(os.getenv('CALCULATOR_PRECISION')))

    @staticmethod
    def divide(a, b):
        Operations._validate_input(a)
        Operations._validate_input(b)
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return round(a / b, int(os.getenv('CALCULATOR_PRECISION')))

    @staticmethod
    def power(a, b):
        Operations._validate_input(a)
        Operations._validate_input(b)
        return round(a**b, int(os.getenv('CALCULATOR_PRECISION')))

    @staticmethod
    def root(a, b):
        Operations._validate_input(a)
        Operations._validate_input(b)
        return round(a ** (1 / b), int(os.getenv('CALCULATOR_PRECISION')))

    @staticmethod
    def modulus(a, b):
        Operations._validate_input(a)
        Operations._validate_input(b)
        return round(a % b, int(os.getenv('CALCULATOR_PRECISION')))

    @staticmethod
    def integer_division(a, b):
        Operations._validate_input(a)
        Operations._validate_input(b)
        return round(a // b, int(os.getenv('CALCULATOR_PRECISION')))

    @staticmethod
    def percentage(a, b):
        Operations._validate_input(a)
        Operations._validate_input(b)
        return round(a * b / 100, int(os.getenv('CALCULATOR_PRECISION')))

    @staticmethod
    def absolute_difference(a, b):
        Operations._validate_input(a)
        Operations._validate_input(b)
        return round(abs(a - b), int(os.getenv('CALCULATOR_PRECISION')))
    
    
