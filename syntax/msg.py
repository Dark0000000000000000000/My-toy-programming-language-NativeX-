def handle(line, vars, out):
    if not line.startswith("msg"):
        return False

    inside = line[3:].strip()
    value = eval(inside, {}, vars)
    out.insert("end", str(value) + "\n")
    return True