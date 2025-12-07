# NativeX IDE - Enhanced Version with Syntax Plugins Only
# Author: Dark

import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import os
import importlib.util
import traceback
import shlex

# ---------------- Paths / Globals ----------------
SYNTAX_DIR = "syntax"
variables = {}
syntax_handlers = []
execution_state = {
    'running': False,
    'paused_for_input': False,
    'current_line_index': 0,
    'lines': [],
    'input_var': None,
    'input_start_index': None,
    'labels': {}
}

# ---------------- Utility: eval wrapper ----------------
def eval_expr(expr):
    try:
        expr = expr.replace('&&', ' and ').replace('||', ' or ')
        return eval(expr, {"__builtins__": None}, variables)
    except Exception as e:
        return f"Error: {e}"

# ---------------- Module Loaders ----------------
def load_syntax_modules(output_widget=None):
    global syntax_handlers
    syntax_handlers = []
    os.makedirs(SYNTAX_DIR, exist_ok=True)

    if output_widget:
        output_widget.config(state='normal')
        output_widget.insert(tk.END, '--- Reloading Syntax Modules ---\n')

    for fname in os.listdir(SYNTAX_DIR):
        if fname.endswith('.py'):
            path = os.path.join(SYNTAX_DIR, fname)
            name = f"syntax_{fname[:-3]}"
            try:
                spec = importlib.util.spec_from_file_location(name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'handle') and callable(module.handle):
                    syntax_handlers.append(module.handle)
                    if output_widget:
                        output_widget.insert(tk.END, f"  Loaded: {fname}\n")
                elif output_widget:
                    output_widget.insert(tk.END, f"⚠ {fname}: 'handle' function not found.\n")
            except Exception as e:
                if output_widget:
                    output_widget.insert(tk.END, f"Error loading {fname}: {e}\n")
                    output_widget.insert(tk.END, traceback.format_exc() + '\n')

    if output_widget:
        output_widget.config(state='disabled')

# ---------------- CORE EXECUTION CONTROL ----------------
def start_execution(code, output_widget):
    global execution_state
    if execution_state['running']:
        output_widget.config(state='normal')
        output_widget.insert(tk.END, '⚠ Error: Code is already running!\n')
        output_widget.config(state='disabled')
        return

    output_widget.config(state='normal')
    output_widget.delete('1.0', tk.END)

    execution_state['lines'] = code.splitlines()
    execution_state['current_line_index'] = 0
    execution_state['running'] = True
    execution_state['paused_for_input'] = False
    execution_state['input_var'] = None
    execution_state['input_start_index'] = None
    execution_state['labels'] = {}

    for i, raw_line in enumerate(execution_state['lines']):
        line = raw_line.strip()
        if line.startswith(':'):
            label_name = line[1:].strip().lower()
            execution_state['labels'][label_name] = i

    variables.setdefault('app_window', None)
    variables['eval_expr'] = eval_expr
    variables['execution_state'] = execution_state

    output_widget.unbind('<Return>')
    output_widget.config(insertbackground='white')

    run_next_line(output_widget)

def run_next_line(output_widget):
    global execution_state
    while execution_state['running'] and execution_state['current_line_index'] < len(execution_state['lines']):
        if execution_state['paused_for_input']:
            return

        raw_line = execution_state['lines'][execution_state['current_line_index']]
        line = raw_line.strip()
        execution_state['current_line_index'] += 1

        if not line or line.startswith('#'):
            continue

        handled = False
        for handler in syntax_handlers:
            try:
                if handler(line, variables, output_widget):
                    handled = True
                    break
            except Exception as e:
                output_widget.insert(tk.END, f"Error in syntax module: {e}\n")
                output_widget.insert(tk.END, traceback.format_exc() + '\n')
                execution_state['running'] = False
                return

        if handled:
            if execution_state['paused_for_input']:
                output_widget.config(state='normal')
                output_widget.insert(tk.END, f"{raw_line} -> ")
                execution_state['input_start_index'] = output_widget.index(tk.END)
                output_widget.config(state='normal')
                output_widget.focus_set()
                output_widget.bind('<Return>', lambda event: handle_input(event, output_widget))
                return
            continue

        if line.startswith('print'):
            val = eval_expr(line[5:].strip())
            output_widget.insert(tk.END, str(val) + '\n')
            continue

        if '=' in line:
            try:
                var, expr = line.split('=', 1)
                variables[var.strip()] = eval_expr(expr.strip())
            except Exception as e:
                output_widget.insert(tk.END, f"Assignment Error: {e}\n")
            continue

        res = eval_expr(line)
        if isinstance(res, str) and res.startswith('Error:'):
            output_widget.insert(tk.END, f"Syntax Error: Unknown command or invalid expression: {line}\n")

    execution_state['running'] = False
    output_widget.insert(tk.END, '\n--- Execution Finished ---\n')
    output_widget.config(state='disabled')
    output_widget.unbind('<Return>')

def handle_input(event, output_widget):
    global execution_state
    input_text = output_widget.get(execution_state['input_start_index'], tk.END).strip()
    output_widget.unbind('<Return>')
    output_widget.mark_set(tk.INSERT, tk.END)

    if execution_state['input_var']:
        variables[execution_state['input_var']] = input_text

    execution_state['paused_for_input'] = False
    execution_state['input_var'] = None
    execution_state['input_start_index'] = None
    output_widget.config(state='disabled')
    run_next_line(output_widget)
    return 'break'

# ---------------- Project Loader ----------------
def load_project():
    path = filedialog.askopenfilename(filetypes=[("NativeX Project", "*.nx")])
    if not path: return
    try:
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open project: {e}")
        return

    code_input.delete('1.0', tk.END)
    code_input.insert(tk.END, code)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("NativeX IDE")
FONT = ("Consolas", 12)
BG_COLOR, FG_COLOR = "#1e1e1e", "#d4d4d4"

code_input = scrolledtext.ScrolledText(root, width=80, height=20, font=FONT, bg=BG_COLOR, fg=FG_COLOR, insertbackground='white')
code_input.pack(padx=10, pady=10)

output_label = tk.Label(root, text="Output:", font=FONT)
output_label.pack()
output_display = scrolledtext.ScrolledText(root, width=80, height=12, font=FONT, bg=BG_COLOR, fg=FG_COLOR, state='disabled', insertbackground='white')
output_display.pack(padx=10, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

run_button = tk.Button(button_frame, text="Run", command=lambda: start_execution(code_input.get('1.0', tk.END), output_display))
run_button.pack(side=tk.LEFT, padx=5)

load_button = tk.Button(button_frame, text="Load Project", command=load_project)
load_button.pack(side=tk.LEFT, padx=5)

reload_syntax_button = tk.Button(button_frame, text="Reload Syntax", command=lambda: load_syntax_modules(output_display))
reload_syntax_button.pack(side=tk.LEFT, padx=5)

open_syntax_dir_button = tk.Button(button_frame, text="Open syntax folder", command=lambda: os.startfile(os.path.abspath(SYNTAX_DIR)) if os.path.isdir(SYNTAX_DIR) else messagebox.showinfo("Info", f"No {SYNTAX_DIR} folder"))
open_syntax_dir_button.pack(side=tk.LEFT, padx=5)

variables['root'] = root
variables['execution_state'] = execution_state

load_syntax_modules(output_display)
os.makedirs(SYNTAX_DIR, exist_ok=True)

root.mainloop()
