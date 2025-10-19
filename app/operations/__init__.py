class Operations:

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    @staticmethod
    def power(a, b):
        return a**b

    @staticmethod
    def root(a, b):
        return a ** (1 / b)

    @staticmethod
    def modulus(a, b):
        return a % b

    @staticmethod
    def integer_division(a, b):
        return a // b

    @staticmethod
    def percentage(a, b):
        return a * b / 100

    @staticmethod
    def absolute_difference(a, b):
        return abs(a - b)
    
    
