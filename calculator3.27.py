import math
import tkinter as tk
from tkinter import messagebox


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.configure(background="#006400")

        self.result_var = tk.StringVar()
        self.result_var.set("0")

        self.input_var = tk.StringVar()
        self.input_var.set("")

        self.create_widgets()

    def create_widgets(self):
        result_label = tk.Label(
            self,
            textvariable=self.result_var,
            font=("Arial", 16),
            anchor="e",
            padx=10,
            pady=10,
            bg="#006400",
            fg="#ffffff",
        )
        result_label.grid(row=0, column=1, columnspan=4)

        help_button = tk.Button(
            self,
            text="?",
            width=3,
            height=2,
            font=("Arial", 14),
            bg="#D6FFB7",
            fg="#000000",
            command=self.open_help_file,
        )
        help_button.grid(row=0, column=0)

        input_entry = tk.Entry(
            self,
            textvariable=self.input_var,
            font=("Arial", 16),
            justify="right",
            bg="#007800",
            fg="#ffffff",
        )
        input_entry.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

        buttons = [
            ("7", 2, 0),
            ("8", 2, 1),
            ("9", 2, 2),
            ("+", 2, 3),
            ("4", 3, 0),
            ("5", 3, 1),
            ("6", 3, 2),
            ("-", 3, 3),
            ("1", 4, 0),
            ("2", 4, 1),
            ("3", 4, 2),
            ("*", 4, 3),
            ("0", 5, 0),
            (".", 5, 1),
            ("=", 5, 2),
            ("/", 5, 3),
            ("^", 2, 4),
            ("ln", 3, 4),
            ("lg", 4, 4),
            ("sin", 5, 4),
            ("cos", 2, 5),
            ("tan", 3, 5),
            ("cot", 4, 5),
            ("C", 5, 5),
        ]

        for button_text, row, col in buttons:
            button = tk.Button(
                self,
                text=button_text,
                width=5,
                height=2,
                font=("Arial", 16),
                bg="#D6FFB7",
                fg="#000000",
            )
            button.grid(row=row, column=col, padx=5, pady=5)
            button.configure(command=lambda btn=button_text: self.on_button_click(btn))

    def open_help_file(self):
        try:
            with open("help3.txt", "r") as file:
                help_text = file.read()
                messagebox.showinfo("Calculator Help", help_text)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "The help file 'help2.txt' is not found.")

    def on_button_click(self, btn_text):
        current_input = self.input_var.get()

        if btn_text == "=":
            self.calculate()
        elif btn_text == "C":
            self.input_var.set("")
            self.result_var.set("0")
        else:
            self.input_var.set(current_input + btn_text)

    def calculate(self):
        user_input = self.input_var.get()

        # Replace common mathematical symbols with space-separated tokens
        user_input = user_input.replace("+", " + ")
        user_input = user_input.replace("-", " - ")
        user_input = user_input.replace("*", " * ")
        user_input = user_input.replace("/", " / ")
        user_input = user_input.replace("^", " ^ ")

        # Check for function names and separate them from numeric input
        functions = ["ln", "lg", "sin", "cos", "tan", "cot"]
        for function in functions:
            user_input = user_input.replace(function, " " + function + " ")

        parts = user_input.split()

        try:
            if len(parts) == 3:
                num1 = self.extract_number(parts[0])
                operator = parts[1]
                num2 = self.extract_number(parts[2])
            elif len(parts) == 2:
                operator = parts[0]
                num1 = self.extract_number(parts[1])
            else:
                raise ValueError

        except:
            self.result_var.set("Invalid input")
            return

        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                self.result_var.set("Division by zero not allowed")
                return
            result = num1 / num2
        elif operator == "^":
            result = num1 ** num2
        elif operator == "ln":
            if num1 <= 0:
                self.result_var.set("Invalid input for logarithm")
                return
            result = math.log(num1)
        elif operator == "lg":
            if num1 <= 0:
                self.result_var.set("Invalid input for logarithm")
                return
            result = math.log10(num1)
        elif operator == "sin":
            result = math.sin(math.radians(num1))
        elif operator == "cos":
            result = math.cos(math.radians(num1))
        elif operator == "tan":
            result = math.tan(math.radians(num1))
        elif operator == "cot":
            if math.tan(math.radians(num1)) == 0:
                self.result_var.set("Invalid input for cotangent")
                return
            result = 1 / math.tan(math.radians(num1))

        self.result_var.set(result)

    def extract_number(self, text):
        try:
            return float(text)
        except ValueError:
            num_str = ""
            for char in text:
                if char.isdigit() or char == ".":
                    num_str += char
            return float(num_str)


if __name__ == "__main__":
    calculator = Calculator()
    calculator.mainloop()
