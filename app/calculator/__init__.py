

from typing import List
from app.calculation import Calculation, CalculationFactory


def calculator():

    history: List[Calculation] = []

    """
    This is a basic REPL calculator that can add, subtract, multiply, and divide two numbers.
    """
    
    "I am using the same structure as module2"
    print("\nWelcome to the calculator!\n")
    
    while True:
        user_input = input("Enter operation (add, subtract, multiply, divide) followed by two numbers or exit to quit, history and help: ").strip().lower()
        
        if user_input == "exit":
            print("Thank you for using the calculator. Bye!\n")
            break

        if user_input == "history":
            display_history(history)
            continue

        if user_input == "help":
            display_help()
            continue
        
        input_params = user_input.split()
        if len(input_params) != 3 or input_params[0] not in ["add", "subtract", "multiply", "divide"]:
            print("Invalid input. Please enter an operation followed by two numbers.")
            continue
        
        try:
            operation, num1, num2 = input_params[0], float(input_params[1]), float(input_params[2])
            calc = CalculationFactory.register_calculation(operation, num1, num2)
            history.append(calc)
            result = calc.execute()
            print(f"\nThe result is {result}\n")
        
        except ValueError:
            print("🫤  Enter not a valid number.\n")

        except ZeroDivisionError:
            print("🫠  You know we cannot divide by zero.\n")

        except Exception as e:  
            print("😭  Unexpected error:", e)
            print("\n")

def display_history(history):
    if (len(history) == 0):
        print("\nNo calculations yet.\n")
        return
    print("\nCalculator history: ")
    for i in history:
        print(i)
    print("\n")
def display_help():
    print("⚠️\nType history for history, help for help and exit to exit and 'operation num1 num2' for calculation\n")
