import csv
import os
from datetime import datetime
from typing import List

from app.calculation import Calculation, CalculationFactory
from app.log_logic import log_operation
from dotenv import load_dotenv
load_dotenv()


def process_command(user_input, history, undo_history):
    log_operation(f"user_input: {user_input}")
    if user_input == "exit":
        print("Thank you for using the calculator. Bye!\n")
        return True 

    elif user_input == "history":
        display_history(history)
        return False

    elif user_input == "help":
        display_help()
        return False

    elif user_input == "undo":
        if len(history) > 0:
            undo_history.append(history.pop())
        else:
            print("No history to undo")
        return False

    elif user_input == "redo":
        if len(undo_history) > 0:
            history.append(undo_history.pop())
        else:
            print("No history to redo")
        return False

    elif user_input == "clear":
        history.clear()
        undo_history.clear()
        return False

    elif user_input == "save":
        save_history(history)
        return False

    elif user_input == "load":
        loaded = load_history()
        history.extend(loaded)
        return False

    elif user_input in ["add", "subtract", "multiply", "divide", "power", "root", "absolute difference", "modulus", "percentage", "integer division"]:
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            calc = CalculationFactory.register_calculation(user_input, num1, num2)
            if calc is not None:
                history.append(calc)
                result = calc.execute()
                print(f"\nThe result is {result}\n")
                log_operation(f"The result is {result}")
                if os.getenv('CALCULATOR_AUTO_SAVE', 'false').lower() == 'true':
                    max_hist = int(os.getenv('CALCULATOR_MAX_HISTORY_SIZE') or '1000')
                    if len(history) <= max_hist:
                        save_history(history)
            else:
                print("Invalid operation")
        except ValueError:
            print("🫤  Enter not a valid number.\n")
        except ZeroDivisionError:
            print("🫠  You know we cannot divide by zero.\n")
        except Exception as e:
            print("😭  Unexpected error:", e)
            print("\n")
        return False

    else:
        print("😭Invalid input")
        display_help()
        return False


def calculator():

    history: List[Calculation] = []
    undo_history: List[Calculation] = []

    """
    This is a basic REPL calculator that can add, subtract, multiply, and divide two numbers.
    """

    "I am using the same structure as module2"
    print("\nWelcome to the calculator!\n")

    log_operation("Welcome to the calculator!")

    while True:
        user_input = (
            input(
                "Enter operation(add, subtract, multiply, divide, power, root, modulus, integer divison, percentage, absolute difference) exit, history, undo, redo, help and quit: \n"
            )
            .strip()
            .lower()
        )
        if process_command(user_input, history, undo_history):
            break


def display_history(history):
    if len(history) == 0:
        print("\nNo calculations yet.\n")
        return
    print("\nCalculator history: ")
    for i in history:
        print(i)
    print("\n")


def display_help():
    print("ℹ️  Help")
    print("history for the list of calculations")
    print("help for the help")
    print("operation num1 num2 for the calculation")
    print("power for the power of the number")
    print("root for the root of the number")
    print("modulus for the rmainder when dividing the numbers")
    print("absolute difference for the absolute difference between the numbers")
    print("integer division for the integer division between the numbers")
    print("percentage for finding the percentage")
    print("undo to undo the last operation")
    print("redo to redo the last operation")
    print("clear to clear the history")
    print("save to save the history to a csv file")
    print("load to load the history from a csv file")
    print("exit to quit the calculator")
    print("\n")


def save_history(history):
    history_dir = os.getenv('CALCULATOR_HISTORY_DIR', 'csv_file')
    file_path = os.path.join(history_dir, "calculator.csv")
    
    with open(file_path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Operation", "Operand1", "Operand2", "Result", "Timestamp"])
        for i in history:
            writer.writerow(
                [
                    i.operation,
                    i.a,
                    i.b,
                    i.execute(),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ]
            )


def load_history():
    loaded_calculations = []
    history_dir = os.getenv('CALCULATOR_HISTORY_DIR', 'csv_file')
    file_path = os.path.join(history_dir, "calculator.csv")
    
    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) >= 4:
                    operation = row[0]
                    a = float(row[1])
                    b = float(row[2])

                    calc = CalculationFactory.register_calculation(operation, a, b)
                    loaded_calculations.append(calc)

            print(f"Loaded {len(loaded_calculations)} calculations from {file_path}")
            return loaded_calculations

    except FileNotFoundError:
        print(f"No saved history file found ({file_path})")
        return []
    except Exception as e:
        print(f"Error loading history: {e}")
        return []


if __name__ == "__main__":
    calculator()
