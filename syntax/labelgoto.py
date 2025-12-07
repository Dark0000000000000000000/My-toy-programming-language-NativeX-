def handle(line, variables, output_widget):
    line = line.split('#', 1)[0].strip()

    if line.startswith(':'):
        return True
    return False