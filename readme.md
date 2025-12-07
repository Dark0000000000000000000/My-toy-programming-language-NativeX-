NativeX IDE





NativeX is a lightweight and extensible programming language with its own Python-based IDE and support for syntax plugins. It is designed for rapid prototyping and project creation with the ability to dynamically extend commands via separate modules.

Features

Interpreted language: executes code line by line, supports variables, output, and basic expressions.

Extensible via plugins: each syntax can be implemented as a separate Python file inside the syntax/ folder. New commands are automatically loaded when the IDE starts.

Interactive output: supports print, user input, and displays results in the IDE output window.

Safe execution: code runs with a restricted set of built-in functions to minimize potential errors.

Full repository available: you can download the full repository with all system syntax modules included.

Quick Start

Clone the repository and ensure Python 3 is installed.

Create a syntax/ folder next to NativeX.py and add your command modules, for example:

# syntax/msg.py

def handle(line, vars, out):
if not line.startswith("msg"):
return False
inside = line\[3:].strip()
value = eval(inside, {}, vars)
out.insert("end", str(value) + "\\n")
return True



Run the IDE:

python NativeX.py



Write NativeX code in the editor:

a = 1
msg a



Click Run to execute the code and view the results in the Output window.

Project Structure
NativeX.py           # Main IDE and interpreter
syntax/              # Folder for syntax plugins
msg.py           # Example plugin
projects/            # (optional) NativeX projects

Support and Extension

Create your own command plugins for NativeX and place them in the syntax/ folder.

The IDE automatically reloads new plugins when you click Reload Syntax.

Variables, expressions, and user input are fully supported within the interpreter.

