import tkinter as tk

timers = {}
update_funcs = {}

def handle(line, vars, out):
    parts = line.split()
    if len(parts) == 0:
        return False

    # --- GET ROOT WINDOW SAFELY ---
    root = vars.get("root", None)
    if root is None:
        return False  # GUI еще не создано

    # ---------- TIMER SET ----------
    if parts[0] == "timer":
        if parts[1] == "set":
            name = parts[2].split("=")[1]
            interval = int(parts[3].split("=")[1])
            func = parts[4].split("=")[1]

            def tick():
                if name in timers:
                    if func in vars:
                        vars[func]()
                    root.after(interval, tick)

            timers[name] = True
            root.after(interval, tick)
            return True

        if parts[1] == "stop":
            name = parts[2]
            if name in timers:
                del timers[name]
            return True

    # ---------- UPDATE EVENT (GAME LOOP) ----------
    if parts[0] == "update_event":
        window = parts[1]
        func = parts[2]

        update_funcs[func] = True

        def loop():
            if update_funcs.get(func, False):
                if func in vars:
                    vars[func]()
                root.after(16, loop)   # 60 FPS

        root.after(16, loop)
        return True

    # ---------- STOP UPDATE ----------
    if parts[0] == "stop_update":
        func = parts[1]
        if func in update_funcs:
            del update_funcs[func]
        return True

    return False
