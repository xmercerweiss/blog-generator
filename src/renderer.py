from .documents import HTMLDocument
from . import dateutil


class HTMLRenderer:

    _CONTENT_SEP = " "

    _OPERATOR_MARKER = "#"
    _COMMENT_MARKER = _OPERATOR_MARKER*2

    _TITLE_KEY = "!"
    _DESC_KEY = "$"
    _DATE_KEY = "?"
    _AUTHOR_KEY = "@"

    _INV_OP_ERR_MSG = "Markdown line {}: Invalid operator \"{}\" provided. Did you make a typo?"

    def __init__(self, date_format=dateutil.DATE_TO_STR_FMT):
        self._current_line = None
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
            "I": self._build_linking_func("img", "src", True)
        }
        self._metadata = {
            self._TITLE_KEY: "Untitled",
            self._DESC_KEY: "",
            self._DATE_KEY: dateutil.display_time(dateutil.STR_TO_DATE_FMT),
            self._AUTHOR_KEY: "Anon"
        }

    def _build_tagging_func(self, tag):
        def tagger(content):
            return f"<{tag}>{content}</{tag}>"
        return tagger 

    def _build_replacing_func(self, content):
        def replacer(*_):
            return content
        return replacer

    def _build_linking_func(self, tag, property, is_open=False):
        def linker(text):
            link, *remainder = text.split(self._CONTENT_SEP)
            content = self._CONTENT_SEP.join(remainder)
            if is_open:
                return f"<{tag} {property}=\"{link}\" alt=\"{content}\">"
            return f"<{tag} {property}=\"{link}\">{content}</{tag}>"
        return linker

    def _build_metadata_func(self, key):
        def set_metadata(value):
            if key in self._metadata:
                self._metadata[key] = value
            return ""
        return set_metadata

    def to_html(self, path):
        output = []
        self._current_line = 0
        split_lines = self._get_split_lines(path)
        for split_line in split_lines:
            self._current_line += 1
            result = self._evaluate_line(split_line)
            if len(result) > 0:
                rendered = self._render_metadata(result)
                output.append(rendered)
        content = "\n".join(output)
        return self._build_html_doc(content)

    def _get_split_lines(self, path):
        output = []
        with open(path, "r") as file:
            for line in file.readlines():
                split = line.strip().split(self._CONTENT_SEP)
                output.append(split)
        return output

    def _evaluate_line(self, split_line):
        starter = split_line[0]
        if starter == self._COMMENT_MARKER:
            return ""
        elif starter.startswith(self._OPERATOR_MARKER):
            operator, *content = split_line
            return self._perform_operation_on(operator, content)
        else:
            return self._CONTENT_SEP.join(split_line)

    def _build_html_doc(self, content):
        title = self._metadata[self._TITLE_KEY]
        desc = self._metadata[self._DESC_KEY]
        date = dateutil.to_date_obj(self._metadata[self._DATE_KEY])
        author = self._metadata[self._AUTHOR_KEY]
        output = HTMLDocument(title, desc, date, author)
        output.content = content
        return output

    def _perform_operation_on(self, operator, content):
        output = self._CONTENT_SEP.join(content)
        for op_code in operator[1:]:
            if op_code not in self._OPERATIONS:
                msg = self._INV_OP_ERR_MSG.format(self._current_line, op_code)
                raise ValueError(msg)
            operation = self._OPERATIONS[op_code]
            output = operation(output)
        return output

    def _render_metadata(self, text):
        output = text
        for key, value in self._metadata.items():
            if key == self._DATE_KEY:
                value = dateutil.display_time(self._date_format, value)
            metadata_char = self._OPERATOR_MARKER + key
            output = output.replace(metadata_char, value)
        return output
