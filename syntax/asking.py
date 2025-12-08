import tkinter as tk

def handle(line, variables, output_widget):
    if not line.lower().startswith('asking '):
        return False
    
    try:
        args_line = line[7:].strip()
        if not args_line:
            raise ValueError("Syntax Error: 'Asking' requires a variable name.")

        parts = args_line.split(' ', 1)
        var_name = parts[0].strip()
        prompt = parts[1].strip() if len(parts) > 1 else ""

        if not var_name.isidentifier():
            raise ValueError(f"Syntax Error: '{var_name}' is not a valid variable name.")

        state = variables.get('execution_state')
        if not state:
            raise RuntimeError("Internal Error: execution_state not found.")
            
        if prompt:
            eval_expr = variables.get('eval_expr')
            display_prompt = eval_expr(prompt)
            output_widget.config(state='normal')
            output_widget.insert(tk.END, str(display_prompt))

        state['paused_for_input'] = True
        state['input_var'] = var_name
        
        return True 
        
    except Exception as e:
        output_widget.config(state='normal')
        output_widget.insert(tk.END, f"Error processing 'Asking': {e}\n")
        variables['execution_state']['running'] = False
        return True
