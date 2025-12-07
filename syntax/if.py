import tkinter as tk

def handle(line, variables, output_widget):
    if not line.startswith("if ") or " goto " not in line:
        return False
        
    try:
        _, rest = line.split(" ", 1)
        condition_part, label_part = rest.split(" goto ", 1)
        
        label_name = label_part.strip().lower()
        
        eval_fn = variables.get('eval_expr')
        if not eval_fn:
            raise Exception("Eval function is not accessible.")
            
        result = eval_fn(condition_part)
        
        if result is True:
            state = variables.get('execution_state')
            labels = state.get('labels', {})
            
            if label_name not in labels:
                output_widget.insert(tk.END, f"Error if: label ':{label_name}' not found!\n")
                state['running'] = False 
                return True

            target_index = labels[label_name]
            state['current_line_index'] = target_index 
            
            
        return True
        
    except Exception as e:
        output_widget.insert(tk.END, f"Error in 'if' the syntax: {e}\n")
        variables['execution_state']['running'] = False
        return True