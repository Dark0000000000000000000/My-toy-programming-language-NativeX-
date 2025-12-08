import tkinter as tk

def handle(line, variables, output_widget):
    if not line.startswith("asking"):
        return False

    state = variables.get("execution_state")
    if not state:
        return False

    try:
        content, var_name = line[6:].split("->")
        content = content.strip().strip('"').strip("'")
        var_name = var_name.strip()
    except Exception as e:
        output_widget.config(state='normal')
        output_widget.insert(tk.END, f"Error parsing asking: {e}\n")
        output_widget.config(state='disabled')
        state['running'] = False
        return True

    def submit_input():
        user_input = entry.get()
        variables[var_name] = user_input
        entry.destroy()
        submit_btn.destroy()
        state['paused_for_input'] = False
        run_next_line(output_widget)

    output_widget.config(state='normal')
    output_widget.insert(tk.END, content + "\n")
    output_widget.config(state='disabled')

    root = variables.get("root")
    entry = tk.Entry(root, bg="#333", fg="#fff", insertbackground='white')
    entry.pack(pady=5)
    entry.focus_set()

    submit_btn = tk.Button(root, text="OK", command=submit_input)
    submit_btn.pack(pady=2)

    state['paused_for_input'] = True
    return True

run_next_line = None
