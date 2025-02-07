import os.path

from parser import HTMLParser


class Converter:

    _CONFIG_SEP = "="
    
    _DOMAIN_FORMAT_KEY = "entry_domain_format"
    _INDEX_PATH_KEY = "index_path"
    _INDEX_TEMP_PATH_KEY = "index_template"
    _OUTPUT_FORMAT_KEY = "entry_filename_format"
    _OUTPUT_PATH_KEY = "entry_dest"
    _OUTPUT_TEMP_PATH_KEY = "entry_template"

    _PLACEHOLDER = "*"

    def __init__(self, config_path):
        self._parser = HTMLParser()
        self._config = self._read_config_file(config_path)

    def _read_config_file(self, path):
        output = {}
        with open(path, "r") as file:
            for line in file.readlines():
                key, value = line.strip().split(self._CONFIG_SEP)
                output[key] = value
        return output

    def process(self, markdown_doc_filepaths):
        for path in markdown_doc_filepaths:
            html_content = self._parser.to_html(path)
            html_template = self._get_html_template()
            html_path = self._generate_output_filepath(path)
            html = html_template.replace(self._PLACEHOLDER, html_content)
            self._write_to_file(html_path, html)
            # Get title of entry, save to ordered list
            # Generate url to output file
            # Create ordered association between title and url
        # Generate new blog page using ordered associations
        # Save to blog output page

    def _get_html_template(self):
        template_path = self._config[self._OUTPUT_TEMP_PATH_KEY]
        with open(template_path, "r") as file:
            return file.read()

    def _generate_output_filepath(self, inp_path):
        out_format = self._config[self._OUTPUT_FORMAT_KEY]
        out_dest = self._config[self._OUTPUT_PATH_KEY]
        *_, inp_name = os.path.split(inp_path)
        out_name = out_format.replace(self._PLACEHOLDER, inp_name)
        return os.path.join(out_dest, out_name)

    @staticmethod
    def _write_to_file(path, content):
        with open(path, "w") as file:
            file.write(content)
