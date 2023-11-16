import os
import utils.filehash as filehash
from extractor import *
from models import *

pdf_exts = [".pdf"]
image_exts = [
    ".avif",
    ".webp",
    ".tif",
    ".tiff",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".png",
]
excel_exts = [".xlsx", ".xlsm"]


def explore(base_dirs: list[str], model_path: str):
    for base_dir in base_dirs:
        for root, _, files in os.walk(base_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                input_file_path = os.path.join(root, file)
                if ext in image_exts:
                    ex = ImageOcrExtractor(model_path)
                    extract_and_insert([ex], input_file_path)
                    pass
                if ext in pdf_exts:
                    ex1 = pdftext.PdfTextExtractor()
                    ex2 = pdfocr.PdfOcrExtractor(model_path)
                    extract_and_insert([ex1, ex2], input_file_path)
                if ext in excel_exts:
                    ex1 = ExcelCellExtractor()
                    ex2 = ExcelSharpExtractor()
                    extract_and_insert([ex1, ex2], input_file_path)

def extract_and_insert(extractors: list[pdftext.Extractor], input_file_path: str):
    hash = filehash.calculate_file_hash(input_file_path)
    reg_document_id = document.get_document_id_by_hash(hash)
    reg_file_id = file.get_file_id_by_hash(input_file_path)
    if reg_document_id is None:
        # ドキュメント未登録
        print(f"mitouroku: {input_file_path}")

        document_id = document.insert_document(
            hash, os.path.getsize(input_file_path)
        )
        if reg_file_id is None:
            # ファイルが未登録の場合はファイルの登録
            file_id = file.insert_file(document_id, input_file_path, False)
        else:
            # ファイルが登録済みの場合はファイルとドキュメントの紐付けし直し
            file.update_document_id(reg_file_id, document_id)

        for extractor in extractors:
            extract_result = extractor.extract(input_file_path)
            # 抽出失敗した場合はリターン
            if extract_result is None:
                return

            extract_id = extract.insert_extract_data(
                document_id, extractor.method, extract_result.extract_details
            )

            for search_text in extract_result.search_texts:
                # 短いものはリターン
                if len(search_text.text) <= 0:
                    continue
                search_text_id = search.insert_search_text(
                    extract_id, search_text.text, search_text.details
                )
    else:
        print(f"tourokuzumi: {input_file_path}")
        # ドキュメント登録済み
        if reg_file_id is None:
            file_id = file.insert_file(reg_document_id, input_file_path, False)
