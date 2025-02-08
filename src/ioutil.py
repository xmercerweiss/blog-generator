    
CONFIG_SEP = "="

TRUE_STR = "true"
FALSE_STR = "false"
TRUTH_VALUES = (TRUE_STR, FALSE_STR)


def read_conf_file(path):
    output = {}
    with open(path, "r") as file:
        for line in file.readlines():
            stripped = line.strip()
            if len(stripped) == 0:
                continue
            key, value = stripped.split(CONFIG_SEP)
            output[key] = interpret_string(value)
    return output


def interpret_string(str):
    try:
        n = int(str)
        return n
    except ValueError:
        lower = str.lower().strip()
        if lower in TRUTH_VALUES:
            return lower == TRUE_STR
        return str
