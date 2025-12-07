import tkinter as tk
import shlex

gui_objects = {}

def parse_args(parts):
    args = {}
    for p in parts:
        if '=' in p:
            k, v = p.split('=', 1)
            if v.isdigit():
                v = int(v)
            args[k] = v
    return args


def handle(line, vars, out):
    parts = shlex.split(line)
    if not parts:
        return False

    cmd = parts[0]

    if cmd == "gui_window":
        if len(parts) < 2:
            out.insert("end", "Error: gui_window <name>\n")
            return True

        name = parts[1]
        win = tk.Toplevel(vars["root"])
        win.title(name)

        gui_objects[name] = win
        vars[name] = win
        return True

    if cmd == "gui_label":
        if len(parts) < 3:
            out.insert("end", "Error: gui_label <parent> <text> ...\n")
            return True

        parent, text = parts[1], parts[2]
        args = parse_args(parts[3:])

        win = gui_objects.get(parent)
        if win is None:
            out.insert("end", f"Parent '{parent}' not found\n")
            return True

        lbl = tk.Label(win, text=text)
        
        # Apply params
        x = args.get("x", 0)
        y = args.get("y", 0)
        color = args.get("color", None)
        font = args.get("font", None)

        if color:
            lbl.config(fg=color)
        if font:
            lbl.config(font=font)

        lbl.place(x=x, y=y)

        return True

    # -------- button --------
    if cmd == "gui_button":
        if len(parts) < 3:
            out.insert("end", "Error: gui_button <parent> <text>\n")
            return True

        parent, text = parts[1], parts[2]
        args = parse_args(parts[3:])

        win = gui_objects.get(parent)
        if win is None:
            out.insert("end", f"Parent '{parent}' not found\n")
            return True

        btn = tk.Button(win, text=text)

        x = args.get("x", 0)
        y = args.get("y", 0)
        w = args.get("w", None)
        h = args.get("h", None)
        bg = args.get("bg", None)

        if w:
            btn.config(width=w)
        if h:
            btn.config(height=h)
        if bg:
            btn.config(bg=bg)

        btn.place(x=x, y=y)

        if "id" in args:
            gui_objects[args["id"]] = btn

        return True

    # -------- rectangle --------
    if cmd == "gui_rect":
        parent = parts[1]
        args = parse_args(parts[2:])

        win = gui_objects.get(parent)
        if win is None:
            out.insert("end", f"Parent '{parent}' not found\n")
            return True

        canvas = gui_objects.get(parent + "_canvas")
        if canvas is None:
            canvas = tk.Canvas(win, width=2000, height=2000, bg="white")
            canvas.place(x=0, y=0)
            gui_objects[parent + "_canvas"] = canvas

        x = args.get("x", 0)
        y = args.get("y", 0)
        w = args.get("w", 50)
        h = args.get("h", 50)
        color = args.get("color", "black")

        rect = canvas.create_rectangle(x, y, x+w, y+h, fill=color)

        if "id" in args:
            gui_objects[args["id"]] = (canvas, rect)

        return True

        # -------- EVENTS --------
    if cmd == "gui_event":
        if len(parts) < 4:
            out.insert("end", "Usage: gui_event <obj> <event> <handler>\n")
            return True

        obj_name = parts[1]
        event = parts[2]
        handler = parts[3]

        obj = gui_objects.get(obj_name)
        if obj is None:
            out.insert("end", f"Object '{obj_name}' not found\n")
            return True

        # tkinter event map
        event_map = {
            "click": "<Button-1>",
            "hover": "<Enter>",
            "leave": "<Leave>",
            "press": "<KeyPress>",
        }

        tk_event = event_map.get(event)
        if tk_event is None:
            out.insert("end", f"Unknown event: {event}\n")
            return True

        def callback(e, handler=handler):
            vars["last_event"] = e
            vars["execution_state"]["paused_for_input"] = False
            vars["execution_state"]["current_handler"] = handler

        # Widgets
        if hasattr(obj, "bind"):
            obj.bind(tk_event, callback)
            return True

        # Canvas objects (tuple)
        if isinstance(obj, tuple):
            canvas, obj_id = obj
            canvas.tag_bind(obj_id, tk_event, callback)
            return True

        out.insert("end", f"Object '{obj_name}' cannot receive events\n")
        return True

    return False
