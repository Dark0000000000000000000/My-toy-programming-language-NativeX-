import random

def handle(line, variables, output_widget):
    if " = random " not in line:
        return False
    
    try:
        var, args_expr = line.split(" = random ", 1)
        var = var.strip()
        
        parts = args_expr.split()
        if len(parts) != 2:
            raise ValueError("Is required: <min> <max>")
            
        eval_fn = variables.get('eval_expr', eval) 
        
        min_val = int(eval_fn(parts[0]))
        max_val = int(eval_fn(parts[1]))
        
        random_number = random.randint(min_val, max_val)
        
        variables[var] = random_number
        
        return True
    except Exception as e:
        output_widget.insert(tk.END, f"Error in 'random' the syntax: {e}\n")
        return True