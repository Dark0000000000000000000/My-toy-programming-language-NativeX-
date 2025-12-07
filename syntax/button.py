import tkinter as tk

def handle(line, variables, output_widget):
    if not line.startswith("button "):
        return False

    if variables.get("app_window") is None: 
        output_widget.insert("end", "Error: there is no window for the button!\n") 
        return True

    text = line.split('"')[1]
    tk.Button(variables["app_window"], text=text).pack()

    return True