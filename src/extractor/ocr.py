import os
import tempfile
from .extractor import *
import utils.ocrimage as ocrimage
import utils.pdftoimage as pdftoimage
import utils.multitosingleimages as multitosingleimages
from typing import Literal

class OcrExtractor(Extractor):
    method = 'ocr'
    def __init__(self, document_type: Literal['pdf', 'image'], custom_model_path:str, languages: list[str], min_word_length: int, min_confident: float):
        self.document_type = document_type
        self.custom_model_path = custom_model_path
        self.languages = languages
        self.min_word_length = min_word_length
        self.min_confident = min_confident

    def extract(self, path: str) -> ExtractResult:
        # 一時フォルダを作成
        temp_dir = tempfile.mkdtemp()

        # PDF・画像を一時フォルダに画像として保存
        match self.document_type:
            case 'pdf':
                images = pdftoimage.pdf_to_temp_images(path, temp_dir)
            case 'image':
                images = multitosingleimages.save_pages_as_png(path, temp_dir)
            case _ :
                raise Exception(f'Unmatch type name: {self.document_type}')
        if images is None:
            return None

        # 画像情報に対してOCRを実行
        file_ocr_result, model_language = ocrimage.ocr_on_images(
            images, self.custom_model_path, self.languages
        )

        # 一時フォルダ内の画像を削除
        for image in os.listdir(temp_dir):
            image_path = os.path.join(temp_dir, image)
            os.remove(image_path)

        # 一時フォルダを削除
        os.rmdir(temp_dir)

        search_texts = []
        file_texts = []
        for page, page_ocr_results in enumerate(file_ocr_result):
            page_texts = []
            for ocr_result in page_ocr_results:
                page_details = {
                    "page": page,
                    "pageCount": len(file_ocr_result),
                    "boxes": [[int(x) for x in pos] for pos in ocr_result["boxes"]],
                    "confident": ocr_result["confident"],
                }
                word_search_text = SearchText(ocr_result["text"], SearchTextUnit.word, page_details)
                search_texts.append(word_search_text)
                page_texts.append(ocr_result["text"])
                file_texts.append(ocr_result["text"])

            page_details = {
                "page": page,
                "pageCount": len(file_ocr_result),
            }
            page_search_text = SearchText('\n'.join(page_texts), SearchTextUnit.page, page_details)
            search_texts.append(page_search_text)
        file_details = {
            "pageCount": len(file_ocr_result),
        }
        file_search_text = SearchText('\n'.join(file_texts), SearchTextUnit.file, file_details)
        search_texts.append(file_search_text)
        extract_details = {
            'modelLanguage' : model_language,
            'customModelPath' : self.custom_model_path,
            'languages' : self.languages,
            'minWordLength' : self.min_word_length,
            'minConfident' : self.min_confident,
        }
        return ExtractResult(extract_details, search_texts)
