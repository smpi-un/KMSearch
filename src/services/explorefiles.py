import os
import utils.filehash as filehash
from extractor import *
from models import *
from sqlalchemy.orm import sessionmaker, relationship
from database_engine import engine

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
    # ファイル単位でデータベースセッションを作成
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        reg_document_id = document.get_document_id_by_hash(session, hash)
        reg_file_id = file.get_file_id_by_hash(session, input_file_path)
        if reg_document_id is None:
            # ドキュメント未登録
            print(f"mitouroku: {input_file_path}")

            document_id = document.insert_document(
                session, hash, os.path.getsize(input_file_path)
            )
            if reg_file_id is None:
                # ファイルが未登録の場合はファイルの登録
                file_id = file.insert_file(session, document_id, input_file_path, False)
            else:
                # ファイルが登録済みの場合はファイルとドキュメントの紐付けし直し
                file.update_document_id(session, reg_file_id, document_id)

            for extractor in extractors:
                extract_result = extractor.extract(input_file_path)
                # 抽出失敗した場合はスキップ
                if extract_result is None:
                    # print(f"extract fault. path: {input_file_path}, method: {extractor.method}")
                    continue

                extract_id = extract.insert_extract_data(
                    session, document_id, extractor.method, extract_result.extract_details
                )

                for search_text in extract_result.search_texts:
                    # 短いものはリターン
                    if len(search_text.text.strip()) <= 0:
                        continue
                    search_text_id = search.insert_search_text(
                        session, extract_id, search_text.text, search_text.unit, search_text.details
                    )

        else:
            print(f"tourokuzumi: {input_file_path}")
            # ドキュメント登録済み
            if reg_file_id is None:
                file_id = file.insert_file(session, reg_document_id, input_file_path, False)
        session.commit()
        # セッションをクローズ
        session.close()
    except Exception as e:
        # print(f"{str(e)} path: {input_file_path}")
        print(f"path: {input_file_path}")
        session.rollback()
        session.close()
        raise e
