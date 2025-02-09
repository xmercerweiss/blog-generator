import os.path

from renderer import HTMLRenderer
import ioutil


class DocumentEngine:
    
    _DOMAIN_FORMAT_KEY = "entry_domain_format"
    _INDEX_PATH_KEY = "index_path"
    _INDEX_TEMP_PATH_KEY = "index_template"
    _OUTPUT_FORMAT_KEY = "entry_filename_format"
    _OUTPUT_DEST_KEY = "entry_dest"
    _OUTPUT_TEMP_PATH_KEY = "entry_template"
    _EXPAND_TABS_KEY = "expand_tabs"

    _TAB_WIDTH = 4
    _SPACE = " "
    _TAB = "\t"
    _PLACEHOLDER = "*"

    _INV_ENTRY_TEMP_ERR_MSG = \
            f"Given entry template does not include content placeholder \"{_PLACEHOLDER}\"; check file path?"

    # I don't like unpacking all the config values
    # in the init like this, but it's less verbose and
    # more readable than referencing the dict values
    # directly. Forgive me.
    def __init__(self, config_path):
        self._parser = HTMLRenderer()
        self._config = ioutil.read_conf_file(config_path)
        self._domain_format = self._config[self._DOMAIN_FORMAT_KEY]
        self._index_path = self._config[self._INDEX_PATH_KEY]
        self._index_template_path = self._config[self._INDEX_TEMP_PATH_KEY]
        self._output_format = self._config[self._OUTPUT_FORMAT_KEY]
        self._output_destination = self._config[self._OUTPUT_DEST_KEY]
        self._ouput_template_path = self._config[self._OUTPUT_TEMP_PATH_KEY]
        self._expand_tabs = self._config[self._EXPAND_TABS_KEY]

    def process(self, markdown_paths):
        for path in markdown_paths:
            content = self._parser.to_html(path)
            template = self._get_html_template()
            html = self._insert_html_content(content, template)
            output_path = self._generate_output_filepath(path)
            url = self._generate_output_url(output_path)
            ioutil.write_to_file(output_path, html)
            # Get title of entry, save to ordered list
            # Create ordered association between title and url
        # Generate new blog page using ordered associations
        # Save to blog output page

    def _get_html_template(self):
        with open(self._ouput_template_path, "r") as file:
            template = file.read()
        if template.find(self._PLACEHOLDER) < 0:
            raise ValueError(self._INV_ENTRY_TEMP_ERR_MSG)
        else:
            return template

    def _insert_html_content(self, content, template):
            tabs = self._count_tabs_before(self._PLACEHOLDER, template)
            tabbed_content = content.replace("\n", f"\n{self._TAB*tabs}")
            result = template.replace(self._PLACEHOLDER, tabbed_content)
            output = self._expand_tabs_in(result) if self._expand_tabs \
                else self._contract_tabs_in(result)
            return output

    def _generate_output_filepath(self, input_path):
        *_, input_name = os.path.split(input_path)
        output_name = self._output_format.replace(self._PLACEHOLDER, input_name)
        return os.path.join(self._output_destination, output_name)

    def _generate_output_url(self, path):
        *_, filename = os.path.split(path)
        output = self._domain_format.replace(self._PLACEHOLDER, filename)
        return output

    def _count_tabs_before(self, char, text):
        text = text.replace(self._SPACE*self._TAB_WIDTH, self._TAB)
        output = 0
        i = text.find(char) - 1
        while text[i] == self._TAB:
            output += 1
            i -= 1
        return output

    def _expand_tabs_in(self, text):
        return text.replace(self._TAB, self._SPACE*self._TAB_WIDTH)

    def _contract_tabs_in(self, text):
        return text.replace(self._SPACE*self._TAB_WIDTH, self._TAB)
