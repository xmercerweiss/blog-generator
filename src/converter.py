
class Converter:

    _CONFIG_SEP = "="
    
    _DOMAIN_FORMAT_KEY = "entry_domain_format"
    _INDEX_PATH_KEY = "index_path"
    _INDEX_TEMP_PATH_KEY = "index_template"
    _OUTPUT_FORMAT_KEY = "entry_filename_format"
    _OUTPUT_PATH_KEY = "entry_dest"
    _OUTPUT_TEMP_PATH_KEY = "entry_template"

    def __init__(self, config_path):
        _config = self._read_config_file(config_path)

    def _read_config_file(self, path):
        output = {}
        with open(path, "r") as file:
            for line in file.readlines():
                key, value = line.strip().split(self._CONFIG_SEP)
                output[key] = value
        return output

    def process(self, markdown_docs):
        for doc in markdown_docs:
            pass
            # Parse, generate HTML content
            # Generate output filename
            # Fill template with content, save to output
            # Get title of entry, save to ordered list
            # Generate url to output file
            # Create ordered association between title and url
        # Generate new blog page using ordered associations
        # Save to blog output page
