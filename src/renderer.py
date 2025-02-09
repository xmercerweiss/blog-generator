import dateutil


class HTMLRenderer:

    _CONTENT_SEP = " "

    _SPECIAL_CHAR = "#"
    _COMMENT_CHAR = _SPECIAL_CHAR*2

    _TITLE_KEY = "!"
    _DESC_KEY = "$"
    _DATE_KEY = "?"
    _AUTHOR_KEY = "@"

    _INV_OP_ERR_MSG = "Invalid operator \"{}\" provided. Did you make a typo?"

    def __init__(self, date_format=dateutil.DATE_TO_STR_FMT):
        self._date_format = date_format
        self._OPERATIONS = {
            self._TITLE_KEY: self._build_metadata_func(self._TITLE_KEY),
            self._DESC_KEY: self._build_metadata_func(self._DESC_KEY),
            self._DATE_KEY: self._build_metadata_func(self._DATE_KEY),
            self._AUTHOR_KEY: self._build_metadata_func(self._AUTHOR_KEY),
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
        self._metadata = {
            self._TITLE_KEY: "Untitled",
            self._DESC_KEY: "",
            self._DATE_KEY: dateutil.display_time(self._date_format),
            self._AUTHOR_KEY: "Anon"
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
            if is_closed:
                return f"<{tag} {property}=\"{link}\">{content}</{tag}>"
            else:
                return f"<{tag} {property}=\"{link}\" alt=\"{content}\">"
        return linker

    def _build_metadata_func(self, key):
        def set_metadata(value):
            if key in self._metadata:
                self._metadata[key] = value
            return ""
        return set_metadata

    def to_html(self, path):
        output = []
        lines = self._get_split_lines(path)
        for line in lines:
            if line[0] == self._COMMENT_CHAR:
                continue
            elif line[0].startswith(self._SPECIAL_CHAR):
                content = self._evaluate_line(*line)
            else:
                content = self._CONTENT_SEP.join(line)
            if len(content) == 0:
                continue
            rendered = self._insert_metadata(content)
            output.append(rendered)
        return "\n".join(output)

    def _get_split_lines(self, path):
        output = []
        with open(path, "r") as file:
            for line in file.readlines():
                clean = line.strip().split(self._CONTENT_SEP)
                output.append(clean)
        return output

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

    def _insert_metadata(self, text):
        output = text
        for key, value in self._metadata.items():
            value = dateutil.display_time(self._date_format, value) if key == self._DATE_KEY else value
            metadata_char = self._SPECIAL_CHAR + key
            output = output.replace(metadata_char, value)
        return output
