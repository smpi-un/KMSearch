from .extractor import *

class ExcelSharpExtractor(Extractor):
    method = 'excelSharp'
    def __init__(self):
        pass
    def extract(self, path: str) -> ExtractResult:
        search_text = []
        extract_details = {
        }
        pass
        return ExtractResult(extract_details, search_text)