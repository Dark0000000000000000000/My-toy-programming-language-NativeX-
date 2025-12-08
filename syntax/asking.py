import tkinter as tk

def handle(line, variables, output_widget):
    if not line.startswith("asking"):
        return False

    state = variables.get("execution_state")
    if not state:
        return False

    content = line[6:].strip().strip('"').strip("'")

    def submit_input(event=None):
        user_input = entry.get()
        variables['last_input'] = user_input
        entry.destroy()
        submit_btn.destroy()
        state['paused_for_input'] = False
        if 'run_next_line' in variables and variables['run_next_line']:
            variables['run_next_line'](output_widget)

    output_widget.config(state='normal')
    output_widget.insert(tk.END, content + "\n")
    output_widget.config(state='disabled')

    root = variables.get("root")
    entry = tk.Entry(root, bg="#333", fg="#fff", insertbackground='white')
    entry.pack(pady=5)
    entry.focus_set()
    entry.bind("<Return>", submit_input)

    submit_btn = tk.Button(root, text="OK", command=submit_input)
    submit_btn.pack(pady=2)

    state['paused_for_input'] = True
    return True
