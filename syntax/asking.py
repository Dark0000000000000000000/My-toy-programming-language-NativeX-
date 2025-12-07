import tkinter as tk
import shlex

def handle(line, variables, output_widget):
    if " = asking " not in line:
        return False
    
    try:
        var, prompt_expr = line.split(" = asking ", 1)
        var = var.strip()
        
        parts = shlex.split(prompt_expr.strip())
        prompt_text = parts[0] if parts else "Enter the value:"
            
        output_widget.insert(tk.END, prompt_text)
        
        
        
        if 'execution_state' in variables:
            state = variables['execution_state']
        else:
            state = {} 

        variables['execution_state']['paused_for_input'] = True
        variables['execution_state']['input_var'] = var
        
        return True
    
    except Exception as e:
        output_widget.insert(tk.END, f"Error in 'asking' the syntax: {e}\n")
        return True