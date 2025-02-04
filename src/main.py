import os.path
import sys

import converter as conv


CONFIG_PATH = "src/CONF"

NO_INPUT_ERR_MSG = "No input files given"
INV_INPUT_ERR_MSG = "Invalid filepath given, did you make a typo?"


def main():
    app = conv.Converter(CONFIG_PATH)
    files_in = sys.argv[1:]
    validate_inputs(files_in)
    app.process(files_in)


def validate_inputs(filepaths):
    if len(filepaths) == 0:
        raise TypeError(NO_INPUT_ERR_MSG)
    for f in filepaths:
        if not os.path.isfile(f):
            raise FileNotFoundError(INV_INPUT_ERR_MSG)


if __name__ == "__main__":
    main()
