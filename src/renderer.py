
class HTMLRenderer:

    _CONTENT_SEP = " "
    _SPECIAL_CHAR = "#"
    _COMMENT_CHAR = _SPECIAL_CHAR*2

    _INV_OP_ERR_MSG = "Invalid operator \"{}\" provided. Did you make a typo?"

    def __init__(self):
        self._OPERATIONS = {
            "1": self._build_tagging_func("h1"),
            "2": self._build_tagging_func("h2"),
            "3": self._build_tagging_func("h3"),
            "4": self._build_tagging_func("h4"),
            "5": self._build_tagging_func("h5"),
            "6": self._build_tagging_func("h6"),
            "/": self._build_tagging_func("em"),
            "_": self._build_tagging_func("strong"),
            "+": self._build_replacing_func("<p>"),
            "-": self._build_replacing_func("</p>"),
            "~": self._build_replacing_func("<hr>"),
            "n": self._build_replacing_func("<br>"),
            "=": self._build_linking_func("a", "href"),
            "I": self._build_linking_func("img", "src", False)
        }

    def _build_tagging_func(self, tag):
        def tagger(content):
            return f"<{tag}>{content}</{tag}>"
        return tagger 

    def _build_replacing_func(self, new):
        def replacer(*_):
            return new
        return replacer

    def _build_linking_func(self, tag, property, is_closed=True):
        def linker(text):
            split = text.split(self._CONTENT_SEP)
            link = split[0]
            content = self._CONTENT_SEP.join(split[1:])
            print(repr(content))
            if is_closed:
                return f"<{tag} {property}=\"{link}\">{content}</{tag}>"
            else:
                return f"<{tag} {property}=\"{link}\" alt=\"{content}\">"
        return linker

    def to_html(self, path):
        output = []
        lines = self._get_split_lines(path)
        for line in lines:
            if line[0] == self._COMMENT_CHAR:
                continue
            elif line[0].startswith(self._SPECIAL_CHAR):
                rendered = self._evaluate_line(*line)
            else:
                rendered = self._CONTENT_SEP.join(line)
            output.append(rendered)
        return "\n".join(output)

    def _evaluate_line(self, *line):
        operator, *content = line
        output = self._CONTENT_SEP.join(content)
        for op in operator[1:]:
            try:
                operation = self._OPERATIONS[op]
                output = operation(output)
            except KeyError:
                msg = self._INV_OP_ERR_MSG % op
                raise ValueError(msg)
        return output

    def _get_split_lines(self, path):
        output = []
        with open(path, "r") as file:
            for line in file.readlines():
                clean = line.strip().split(self._CONTENT_SEP)
                output.append(clean)
        return output
