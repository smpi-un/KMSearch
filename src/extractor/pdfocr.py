import os
import tempfile
from .extractor import *
import services.ocrimage as ocrimage
import services.pdftoimage as pdftoimage

class PdfOcrExtractor(Extractor):
    method = 'pdfOcr'
    def __init__(self, custom_model_path = ''):
        self.custom_model_path = custom_model_path
    def extract(self, path: str) -> ExtractResult:
        # 一時フォルダを作成
        temp_dir = tempfile.mkdtemp()

        # PDF・画像を一時フォルダに画像として保存
        images = pdftoimage.pdf_to_temp_images(path, temp_dir)

        # 画像情報に対してOCRを実行
        file_ocr_result, model_language, custom_model_path = ocrimage.ocr_on_images(
            images[0:2], self.custom_model_path
        )

        # 一時フォルダ内の画像を削除
        for image in os.listdir(temp_dir):
            image_path = os.path.join(temp_dir, image)
            os.remove(image_path)

        # 一時フォルダを削除
        os.rmdir(temp_dir)

        search_texts = []
        for page, page_ocr_results in enumerate(file_ocr_result):
            for ocr_result in page_ocr_results:
                details = {
                    "page": page,
                    "boxes": [[int(x) for x in pos] for pos in ocr_result["boxes"]],
                    "confident": ocr_result["confident"],
                }
                search_text = SearchText(ocr_result["text"], details)
                search_texts.append(search_text)
                # print(ocr_json)
        extract_details = {
            'customModelPath': self.custom_model_path,
            'model_language' : model_language,
            'custom_model_path' : custom_model_path,
        }
        return ExtractResult(extract_details, search_texts)
