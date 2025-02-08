import os.path
import sys

import engine 


CONFIG_PATH = "test/myconf"

NO_INPUT_ERR_MSG = "No input files given"
INV_INPUT_ERR_MSG = "Invalid filepath given, did you make a typo?"


def main():
    app = engine.DocumentEngine(CONFIG_PATH)
    input_paths = sys.argv[1:]
    validate_inputs(input_paths)
    app.process(input_paths)


def validate_inputs(paths):
    if len(paths) == 0:
        raise TypeError(NO_INPUT_ERR_MSG)
    for path in paths:
        if not os.path.isfile(path):
            raise FileNotFoundError(INV_INPUT_ERR_MSG)


if __name__ == "__main__":
    main()
