
class HTMLParser:

    _CONTENT_SEP = " "
    _SPECIAL_CHAR = "#"

    def __init__(self):
        self._OPERATIONS = {
            self._SPECIAL_CHAR + "1": self._build_tagging_func("h1"),
            self._SPECIAL_CHAR + "2": self._build_tagging_func("h2"),
            self._SPECIAL_CHAR + "3": self._build_tagging_func("h3"),
            self._SPECIAL_CHAR + "4": self._build_tagging_func("h4"),
            self._SPECIAL_CHAR + "5": self._build_tagging_func("h5"),
            self._SPECIAL_CHAR + "6": self._build_tagging_func("h6"),
        }

    def _build_tagging_func(self, tag):
        def tagger(*args):
            content = self._CONTENT_SEP.join(args)
            return f"<{tag}>{content}</{tag}>"
        return tagger 

    def _build_replacement_func(self, new):
        def replacement(*_):
            return new
        return replacement

    def _reflect(content):
        return content

    def to_html(self, path):
        output = []
        lines = self._get_split_lines(path)
        for line in lines:
            operator, *content = line
            operation = self._OPERATIONS[operator] if operator in self._OPERATIONS \
                                                   else self._reflect
            output.append(operation(*content))
        return "\n".join(output)

    def _get_split_lines(self, path):
        output = []
        with open(path, "r") as file:
            for line in file.readlines():
                clean = line.strip().split(self._CONTENT_SEP)
                output.append(clean)
        return output
