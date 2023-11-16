import fitz  # PyMuPDF
from .extractor import *


class PdfTextExtractor(Extractor):
    method = 'pdfText'
    def extract(self, path: str) -> ExtractResult | None:
        search_text = []
        extract_details = {
            'library': 'PyMuPDF'
        }
        with fitz.open(path) as pdf_document:
            if pdf_document.is_encrypted:
                return None
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text = page.get_text("text")
                if text != '':
                    search_text.append(SearchText(text, {'page': page_num}))
        return ExtractResult(extract_details, search_text)


