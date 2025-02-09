    
CONFIG_SEP = "="

TRUE_STR = "true"
FALSE_STR = "false"
TRUTH_VALUES = (TRUE_STR, FALSE_STR)


def read_conf_file(path):
    output = {}
    with open(path, "r") as file:
        for line in file.readlines():
            stripped = line.strip()
            if len(stripped) > 0:
                key, value = stripped.split(CONFIG_SEP)
                output[key] = interpret_string(value)
    return output


def interpret_string(s):
    try:
        n = int(s)
        return n
    except ValueError:
        lower = s.lower().strip()
        if lower in TRUTH_VALUES:
            return lower == TRUE_STR
        return s


def write_to_file(path, content):
    with open(path, "w") as file:
        file.write(content)
