import csv
from datetime import datetime
from typing import List

from app.calculation import Calculation, CalculationFactory
from app.log_logic import log_operation


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
                "Enter operation(add, subtract, multiply, divide, power, root) exit, history, undo, redo, help and quit: \n"
            )
            .strip()
            .lower()
        )
        log_operation(f"user_input: {user_input}")
        if user_input == "exit":
            print("Thank you for using the calculator. Bye!\n")
            break

        elif user_input == "history":
            display_history(history)
            continue

        elif user_input == "help":
            display_help()
            continue

        elif user_input == "undo":
            if len(history) > 0:
                undo_history.append(history.pop())
                continue
            else:
                print("No history to undo")
                continue

        elif user_input == "redo":
            if len(undo_history) > 0:
                history.append(undo_history.pop())
                continue
            else:
                print("No history to redo")
                continue

        elif user_input == "clear":
            history.clear()
            undo_history.clear()
            continue

        elif user_input == "save":
            save_history(history)
            continue

        elif user_input == "load":
            history = load_history()
            continue

        elif user_input in ["add", "subtract", "multiply", "divide", "power", "root"]:

            try:
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))
                calc = CalculationFactory.register_calculation(user_input, num1, num2)
                history.append(calc)
                result = calc.execute()
                print(f"\nThe result is {result}\n")
                log_operation(f"The result is {result}")

            except ValueError:
                print("🫤  Enter not a valid number.\n")

            except ZeroDivisionError:
                print("🫠  You know we cannot divide by zero.\n")

            except Exception as e:
                print("😭  Unexpected error:", e)
                print("\n")

        else:
            print("😭Invalid input")
            display_help()


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
    print("undo to undo the last operation")
    print("redo to redo the last operation")
    print("clear to clear the history")
    print("save to save the history to a csv file")
    print("load to load the history from a csv file")
    print("exit to quit the calculator")
    print("\n")


def save_history(history):
    with open("calculator.csv", "w") as file:
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
    try:
        with open("calculator.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) >= 4:
                    operation = row[0]
                    a = float(row[1])
                    b = float(row[2])

                    calc = CalculationFactory.register_calculation(operation, a, b)
                    loaded_calculations.append(calc)

            print(f"Loaded {len(loaded_calculations)} calculations from calculator.csv")
            return loaded_calculations

    except FileNotFoundError:
        print("No saved history file found (calculator.csv)")
        return []
    except Exception as e:
        print(f"Error loading history: {e}")
        return []


if __name__ == "__main__":
    calculator()
