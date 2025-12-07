def handle(line, vars, out):
    if not line.startswith("repeat"):
        return False

    try:
        parts = line[6:].strip().split(None, 1)
        count = int(parts[0])
        message = parts[1]
        for _ in range(count):
            out.insert("end", message + "\n")
    except:
        out.insert("end", "Error: use repeat <number> <text>\n")
    return True
