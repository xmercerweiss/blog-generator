import os.path
import glob
import sys

from src import DocumentEngine


CONFIG_PATH = "main.conf"

NO_INPUT_ERR_MSG = "No input files given"
INV_INPUT_ERR_MSG = "Invalid filepath given, did you make a typo?"


def main():
    app = DocumentEngine(CONFIG_PATH)
    args = sys.argv[1:]
    valid_paths = validate_paths(args)
    app.process(valid_paths)


def validate_paths(paths):
    output = []
    if len(paths) == 0:
        raise TypeError(NO_INPUT_ERR_MSG)
    for path in paths:
        globbed = glob.glob(path)
        if os.path.isfile(path):
            output.append(path)
        elif len(globbed) > 0:
            output.extend(globbed)
        else:
            raise FileNotFoundError(INV_INPUT_ERR_MSG)
    return output


if __name__ == "__main__":
    main()
