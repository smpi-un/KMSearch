from models.search import SearchTextUnit

class SearchText:
    def __init__(self, text: str, unit: SearchTextUnit, details: any) -> None:
        self.text = text
        self.unit = unit
        self.details = details


class ExtractResult:
    def __init__(self, extract_details: any, search_texts: list[SearchText]) -> None:
        self.extract_details = extract_details
        self.search_texts = search_texts

class Extractor:

    method = None
    def extract(self, path: str) -> ExtractResult | None:
        pass