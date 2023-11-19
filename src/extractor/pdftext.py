import fitz  # PyMuPDF
from .extractor import *


class PdfTextExtractor(Extractor):
    method = 'pdfText'
    def extract(self, path: str) -> ExtractResult | None:
        extract_details = {
            'library': 'PyMuPDF'
        }
        with fitz.open(path) as pdf_document:
            if pdf_document.is_encrypted:
                return None
            search_texts = []
            file_texts = []
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text = page.get_text("text")
                if text != '':
                    word_details = {
                        'page': page_num,
                        'pageCount': pdf_document.page_count,
                    }
                    search_texts.append(SearchText(text, SearchTextUnit.word, word_details))
                    search_texts.append(SearchText(text, SearchTextUnit.page, word_details))
                    file_texts.append(text)
                    
            file_details = {
                'pageCount': pdf_document.page_count,
            }
            search_texts.append(SearchText('\n'.join(file_texts), SearchTextUnit.file, file_details))
        return ExtractResult(extract_details, search_texts)


