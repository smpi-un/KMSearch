import os
import tempfile
from .extractor import *
import utils.ocrimage as ocrimage
import utils.multitosingleimages as multitosingleimages

class ImageOcrExtractor(Extractor):
    method = 'imageOcr'
    def __init__(self, custom_model_path = ''):
        self.custom_model_path = custom_model_path
    def extract(self, path: str) -> ExtractResult:
        # 一時フォルダを作成
        temp_dir = tempfile.mkdtemp()

        # PDF・画像を一時フォルダに画像として保存
        images = multitosingleimages.save_pages_as_png(path, temp_dir)

        # 画像情報に対してOCRを実行
        file_ocr_result, model_language = ocrimage.ocr_on_images(
            images, self.custom_model_path
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
            'customModelPath': self.custom_model_path,
            'modelLanguage' : model_language,
        }
        return ExtractResult(extract_details, search_texts)

