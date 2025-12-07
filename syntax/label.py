import tkinter as tk

def handle(line, variables, output_widget):
    line = line.split('#', 1)[0].strip()
    
    if not line.startswith("if ") or " goto " not in line:
        return False
        
    if variables.get("app_window") is None: 
        output_widget.insert("end", "Error: there is no window for the label!\n") 
        return True

    text = line.split('"')[1]
    tk.Label(variables["app_window"], text=text).pack()

    return True