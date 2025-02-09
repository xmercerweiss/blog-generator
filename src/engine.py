from bisect import insort
import os.path

from .documents import HTMLDocument
from .renderer import HTMLRenderer
from . import ioutil


class DocumentEngine:
    
    _DOMAIN_FORMAT_KEY = "entry_domain_format"
    _INDEX_PATH_KEY = "index_path"
    _INDEX_TEMP_PATH_KEY = "index_template"
    _ENTRY_FORMAT_KEY = "entry_filename_format"
    _ENTRY_DEST_KEY = "entry_dest"
    _ENTRY_TEMP_PATH_KEY = "entry_template"
    _DATE_FORMAT_KEY = "date_format"
    _NEWEST_FIRST_KEY = "newest_first"
    _EXPAND_TABS_KEY = "expand_tabs"

    _TAB_WIDTH = 4
    _SPACE = " "
    _TAB = "\t"

    _TEMPLATE_PLACEHOLDER = "#CONTENT#"
    _VALUE_PLACEHOLDER = "*"

    _INDEX_ENTRY_FORMAT = "<li><a href=\"{}\">{}</a></li>"

    _INV_TEMP_ERR_MSG = \
            f"Given template does not include content placeholder \"{_TEMPLATE_PLACEHOLDER}\"; check file path?"

    # I don't like unpacking all the config values
    # in the init like this, but it's less verbose and
    # more readable than referencing the dict values
    # directly. Forgive me.
    def __init__(self, config_path):
        self._config = ioutil.read_conf_file(config_path)
        self._domain_format = self._config[self._DOMAIN_FORMAT_KEY]
        self._index_path = self._config[self._INDEX_PATH_KEY]
        self._index_template_path = self._config[self._INDEX_TEMP_PATH_KEY]
        self._entry_format = self._config[self._ENTRY_FORMAT_KEY]
        self._entry_destination = self._config[self._ENTRY_DEST_KEY]
        self._entry_template_path = self._config[self._ENTRY_TEMP_PATH_KEY]
        self._date_format = self._config[self._DATE_FORMAT_KEY]
        self._newest_first = self._config[self._NEWEST_FIRST_KEY]
        self._expand_tabs = self._config[self._EXPAND_TABS_KEY]

        self._renderer = HTMLRenderer(self._date_format)

    def process(self, markdown_paths):
        docs_by_date = []
        for path in markdown_paths:
            doc = self._generate_html_doc_from(path)
            entry_path = self._generate_entry_path(path)
            doc.url = self._generate_entry_url(entry_path)
            insort(docs_by_date, doc, key=lambda d: d.date)
            doc.export_to(entry_path)
        if self._newest_first:
             docs_by_date.reverse()
        index = self._generate_html_index_of(docs_by_date)
        index.export_to(self._index_path)

    def _generate_html_doc_from(self, markdown_path):
            html_doc = self._renderer.to_html(markdown_path)
            template = self._get_html_template(self._entry_template_path)
            html_doc.content = self._insert_html_content(html_doc.content, template)
            return html_doc

    def _generate_entry_path(self, markdown_path):
        *_, markdown_name = os.path.split(markdown_path)
        entry_name = self._entry_format.replace(self._VALUE_PLACEHOLDER, markdown_name)
        return os.path.join(self._entry_destination, entry_name)

    def _generate_entry_url(self, path):
        *_, entry_name = os.path.split(path)
        output = self._domain_format.replace(self._VALUE_PLACEHOLDER, entry_name)
        return output

    def _generate_html_index_of(self, docs):
        output = HTMLDocument()
        entries = self._docs_to_html_list(docs)
        template = self._get_html_template(self._index_template_path)
        content = self._insert_html_content(entries, template)
        output.content = content
        return output

    def _get_html_template(self, path):
        with open(path, "r") as file:
            template = file.read()
        if template.find(self._TEMPLATE_PLACEHOLDER) < 0:
            raise ValueError(self._INV_TEMP_ERR_MSG)
        else:
            return template

    def _insert_html_content(self, content, template):
            tabs = self._count_tabs_before(self._TEMPLATE_PLACEHOLDER, template)
            tabbed_content = content.replace("\n", f"\n{self._TAB*tabs}")
            result = template.replace(self._TEMPLATE_PLACEHOLDER, tabbed_content)
            output = self._expand_tabs_in(result) if self._expand_tabs \
                else self._shrink_tabs_in(result)
            return output
    
    def _docs_to_html_list(self, docs):
        output = ["<ol>", "</ol>"]
        for doc in docs:
            entry = self._INDEX_ENTRY_FORMAT.format(doc.url, doc.title)
            output.insert(1, entry)
        return "\n".join(output)

    def _count_tabs_before(self, s, text):
        text = text.replace(self._SPACE*self._TAB_WIDTH, self._TAB)
        output = 0
        i = text.find(s) - 1
        while text[i] == self._TAB:
            output += 1
            i -= 1
        return output

    def _expand_tabs_in(self, text):
        return text.replace(self._TAB, self._SPACE*self._TAB_WIDTH)

    def _shrink_tabs_in(self, text):
        return text.replace(self._SPACE*self._TAB_WIDTH, self._TAB)
