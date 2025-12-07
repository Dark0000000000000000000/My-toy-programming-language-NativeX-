import tkinter as tk

def handle(line, variables, output_widget):
    line = line.split('#', 1)[0].strip()

    if not line.startswith("goto "):
        return False
        
    try:
        label_name = line[5:].strip().lower()
        
        state = variables.get('execution_state')
        labels = state.get('labels', {})
        
        if label_name not in labels:
            output_widget.insert(tk.END, f"Error goto: label ':{label_name}' not found!\n")
            state['running'] = False 
            return True
        
        target_index = labels[label_name]
        state['current_line_index'] = target_index 
        
        return True
    
    except Exception as e:
        output_widget.insert(tk.END, f"Error in 'goto' the syntax: {e}\n")
        variables['execution_state']['running'] = False
        return True