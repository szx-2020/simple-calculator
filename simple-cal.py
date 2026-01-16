import tkinter as tk
from tkinter import ttk
import ast
import operator as op

# ---------- Safe Math Engine ----------
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.USub: op.neg
}

def safe_eval(expr):
    def eval_(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num): # Support for older Python versions
            return node.n
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](eval_(node.left), eval_(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](eval_(node.operand))
        else:
            raise TypeError(node)
    
    try:
        node = ast.parse(expr, mode='eval').body
        return eval_(node)
    except Exception:
        return "Error"

# ---------- Calculator Page ----------
class CalculatorPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#1e1e1e")
        self.expression = ""
        self.last_expression = ""

        for i in range(6):
            self.rowconfigure(i, weight=1)
        for j in range(4):
            self.columnconfigure(j, weight=1)

        # Display
        display_frame = tk.Frame(self, bg="#1e1e1e")
        display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        display_frame.rowconfigure(0, weight=1)
        display_frame.rowconfigure(1, weight=2)
        display_frame.columnconfigure(0, weight=1)

        self.history_label = tk.Label(
            display_frame,
            text="",
            font=("Arial", 14),
            fg="#aaaaaa",
            bg="#1e1e1e",
            anchor="e"
        )
        self.history_label.grid(row=0, column=0, sticky="e")

        self.main_label = tk.Label(
            display_frame,
            text="0",
            font=("Arial", 32, "bold"),
            fg="white",
            bg="#1e1e1e",
            anchor="e"
        )
        self.main_label.grid(row=1, column=0, sticky="e")

        # Button logic
        def press(key):
            if key == "C":
                self.expression = ""
                self.last_expression = ""
                self.main_label.config(text="0")
                self.history_label.config(text="")
            elif key == "=":
                if self.expression:
                    # Replace visual operators with math operators
                    safe_expr = self.expression.replace("×", "*").replace("÷", "/")
                    result = safe_eval(safe_expr)
                    
                    self.last_expression = self.expression
                    self.expression = str(result)
                    self.main_label.config(text=self.expression)
                    self.history_label.config(text=self.last_expression)
                    
                    if result == "Error":
                        self.expression = ""
            else:
                if self.main_label.cget("text") == "0" or self.main_label.cget("text") == "Error":
                    self.expression = key
                else:
                    self.expression += key
                self.main_label.config(text=self.expression)

        # Styles
        num_style = {"font": ("Arial", 16), "bg": "#2d2d2d", "fg": "white", "bd": 0, "relief": "flat", "activebackground": "#3a3a3a"}
        op_style = {"font": ("Arial", 16), "bg": "#ff9500", "fg": "white", "bd": 0, "relief": "flat", "activebackground": "#ffa733"}
        clear_style = {"font": ("Arial", 16), "bg": "#ff3b30", "fg": "white", "bd": 0, "relief": "flat", "activebackground": "#ff5e57"}

        # Buttons setup
        buttons = [
            ("1", 1, 0, num_style), ("2", 1, 1, num_style), ("3", 1, 2, num_style), ("+", 1, 3, op_style),
            ("4", 2, 0, num_style), ("5", 2, 1, num_style), ("6", 2, 2, num_style), ("-", 2, 3, op_style),
            ("7", 3, 0, num_style), ("8", 3, 1, num_style), ("9", 3, 2, num_style), ("×", 3, 3, op_style),
            ("0", 4, 0, num_style), ("C", 4, 1, clear_style), ("÷", 4, 3, op_style),
        ]

        for (text, row, col, style) in buttons:
            btn = tk.Button(self, text=text, command=lambda t=text: press(t), **style)
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        # "=" button (Fixing the syntax issue here)
        equal_btn = tk.Button(self, text="=", command=lambda: press("="), **op_style)
        equal_btn.grid(row=4, column=2, sticky="nsew", padx=5, pady=5)

# ---------- Main App Setup ----------
root = tk.Tk()
root.title("Dark Calculator Pro")
root.configure(bg="#1e1e1e")
root.minsize(350, 500)

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
style.configure("TNotebook.Tab", background="#2d2d2d", foreground="white", padding=[12, 8])
style.map("TNotebook.Tab", background=[("selected", "#3a3a3a")])

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab_count = 0

def add_tab():
    global tab_count
    tab_count += 1
    page = CalculatorPage(notebook)
    notebook.add(page, text=f"P-{tab_count}")
    notebook.select(page)

def close_current_tab():
    if len(notebook.tabs()) > 1:
        notebook.forget(notebook.select())

add_tab()

bottom_bar = tk.Frame(root, bg="#1e1e1e")
bottom_bar.pack(fill="x", pady=5)

new_tab_btn = tk.Button(bottom_bar, text="+ New Calculator", font=("Arial", 12), bg="#2d2d2d", fg="white", bd=0, command=add_tab)
new_tab_btn.pack(side="left", fill="x", expand=True, padx=5)

close_tab_btn = tk.Button(bottom_bar, text="X Close Current", font=("Arial", 12), bg="#ff3b30", fg="white", bd=0, command=close_current_tab)
close_tab_btn.pack(side="right", fill="x", expand=True, padx=5)

root.mainloop()