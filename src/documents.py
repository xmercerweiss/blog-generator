
class HTMLDocument:

    _INV_STR_ERR_MSG = "Invalid string given"

    def __init__(self, title=None, desc=None, date=None, author=None):
        self._title = title
        self._description = desc
        self._date = date
        self._author = author
        self._content = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise ValueError(self._INV_STR_ERR_MSG)
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError(self._INV_STR_ERR_MSG)
        self._description = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, str):
            raise ValueError(self._INV_STR_ERR_MSG)
        self._date = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, str):
            raise ValueError(self._INV_STR_ERR_MSG)
        self._author = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise ValueError(self._INV_STR_ERR_MSG)
        self._content = value
