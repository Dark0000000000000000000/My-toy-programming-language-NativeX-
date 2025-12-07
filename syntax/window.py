import tkinter as tk

def handle(line, variables, output_widget):
    if not line.startswith("window "):
        return False

    parts = line.split()
    title = line.split('"')[1]
    w, h = map(int, parts[-2:])
    win = tk.Toplevel(variables["root"]) 
    win.title(title)
    win.geometry(f"{w}x{h}")

    variables["app_window"] = win 
    return True