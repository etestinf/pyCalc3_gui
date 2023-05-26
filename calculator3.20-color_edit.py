import math
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter.colorchooser import askcolor


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")

        self.result_var = tk.StringVar()
        self.result_var.set("0")

        self.input_var = tk.StringVar()
        self.input_var.set("")

        self.background_color = "#ffffff"
        self.buttons_color = "#eeeeee"

        self.create_widgets()

    def create_widgets(self):
        result_label = tk.Label(
            self, textvariable=self.result_var, font=("Arial", 16), anchor="e", padx=10, pady=10
        )
        result_label.grid(row=0, column=0, columnspan=5)

        input_entry = tk.Entry(
            self, textvariable=self.input_var, font=("Arial", 16), justify="right"
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
            ("?", 0, 4),
        ]

        for button_text, row, col in buttons:
            if button_text == "?":
                button = tk.Button(
                    self,
                    text=button_text,
                    width=3,
                    height=1,
                    font=("Arial", 10, "bold"),
                    command=self.show_help,
                )
            else:
                button = tk.Button(
                    self,
                    text=button_text,
                    width=5,
                    height=2,
                    font=("Arial", 16),
                    command=lambda btn=button_text: self.on_button_click(btn),
                )
            button.grid(row=row, column=col, padx=5, pady=5)

        # Add color change buttons
        bg_color_button = tk.Button(
            self,
            text="Background",
            width=10,
            height=1,
            font=("Arial", 10),
            command=self.change_background_color,
        )
        bg_color_button.grid(row=6, column=0, padx=5, pady=5)

        buttons_color_button = tk.Button(
            self,
            text="Buttons",
            width=10,
            height=1,
            font=("Arial", 10),
            command=self.change_buttons_color,
        )
        buttons_color_button.grid(row=6, column=1, padx=5, pady=5)

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

        # Check for invalid characters
        if any(char not in "0123456789.+-*/^ " for char in user_input):
            self.result_var.set("Invalid input")
            return

        try:
            parts = user_input.split()
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

    def show_help(self):
        try:
            with open("help2.txt", "r") as file:
                help_text = file.read()
            messagebox.showinfo("Help", help_text)
        except FileNotFoundError:
            messagebox.showinfo("Help", "Help file not found.")

    def change_background_color(self):
        color = askcolor(color=self.background_color)[1]
        if color:
            self.background_color = color
            self.configure(background=self.background_color)

    def change_buttons_color(self):
        color = askcolor(color=self.buttons_color)[1]
        if color:
            self.buttons_color = color
            for button in self.winfo_children():
                if isinstance(button, tk.Button):
                    button.configure(bg=self.buttons_color)

if __name__ == "__main__":
    calculator = Calculator()
    calculator.mainloop()
