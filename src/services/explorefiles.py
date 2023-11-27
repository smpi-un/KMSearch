import os, sys
import utils.filehash as filehash
from extractor import *
from models import *
from sqlalchemy.orm import sessionmaker, relationship
from database_engine import get_engine


def explore(base_dirs: list[str], explore_conf: dict, ocr_conf: dict):
    for base_dir in base_dirs:
        for root, _, files in os.walk(base_dir):
            for file in files:
                input_file_path = os.path.join(root, file)
                extractors = choose_extractors(input_file_path, explore_conf, ocr_conf)
                if extractors is None or extractors == []:
                    continue
                extract_and_insert(extractors, input_file_path)

def choose_extractors(input_file_path: str, explore_conf: dict, ocr_conf: dict) -> list[Extractor]:
    ext = os.path.splitext(input_file_path)[1].lower()
    try:
        filesize = os.path.getsize(input_file_path)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return None
    extractors = []
    # 拡張子で場合分けしてExtractorを生成する。
    if ext in explore_conf['image']['extensions']:
        if explore_conf['image']['ocr']['enabled'] and \
           explore_conf['image']['ocr']['minSize'] <= filesize and \
           explore_conf['image']['ocr']['maxSize'] >= filesize:
            extractors.append(EasyOcrExtractor('image', ocr_conf["modelPath"], ocr_conf['languages'], ocr_conf['minWordLength'], ocr_conf['minConfident']))
    if ext in explore_conf['pdf']['extensions']:
        if explore_conf['pdf']['text']['enabled'] and \
           explore_conf['pdf']['text']['minSize'] <= filesize and \
           explore_conf['pdf']['text']['maxSize'] >= filesize:
            extractors.append(PdfTextExtractor())
        if explore_conf['pdf']['ocr']['enabled'] and \
           explore_conf['pdf']['ocr']['minSize'] <= filesize and \
           explore_conf['pdf']['ocr']['maxSize'] >= filesize:
            extractors.append(EasyOcrExtractor('pdf', ocr_conf["modelPath"], ocr_conf['languages'], ocr_conf['minWordLength'], ocr_conf['minConfident']))
    if ext in explore_conf['excel']['extensions']:
        if explore_conf['excel']['cell']['enabled'] and \
           explore_conf['excel']['cell']['minSize'] <= filesize and \
           explore_conf['excel']['cell']['maxSize'] >= filesize:
            extractors.append(ExcelCellExtractor())
        if explore_conf['excel']['sharp']['enabled'] and \
           explore_conf['excel']['sharp']['minSize'] <= filesize and \
           explore_conf['excel']['sharp']['maxSize'] >= filesize:
            extractors.append(ExcelSharpExtractor())
    return extractors


def extract_and_insert(extractors: list[pdftext.Extractor], input_file_path: str):
    if not os.path.exists(input_file_path):
        return

    try:
        hash = filehash.calculate_file_hash(input_file_path)
    except PermissionError as e:
        print(e, file=sys.stderr)
        return

    filesize = os.path.getsize(input_file_path)
    # ファイル単位でデータベースセッションを作成
    Session = sessionmaker(bind=get_engine())
    session = Session()
    try:
        reg_document = document.get_document_by_hash(session, hash)
        reg_file = file.get_file_by_hash(session, input_file_path)
        if reg_document is None:
            # ドキュメント未登録
            print(f"mitouroku: {input_file_path}", file=sys.stdout)

            document_id = document.insert_document(
                session, hash, filesize
            )
            if reg_file is None:
                # ファイルが未登録の場合はファイルの登録
                file_id = file.insert_file(session, document_id, input_file_path, False)
            else:
                # ファイルが登録済みの場合はファイルとドキュメントの紐付けし直し
                file.update_document_id(session, reg_file.file_id, document_id)

        else:
            print(f"tourokuzumi: {input_file_path}", file=sys.stdout)
            # ドキュメント登録済み
            document_id = reg_document.document_id
            if reg_file is None:
                file_id = file.insert_file(session, reg_document.document_id, input_file_path, False)
        for extractor in extractors:
            if extractor is None:
                continue
            if reg_document is not None and extractor.method in [x.method for x in reg_document.extracts]:
                continue

            extract_result = extractor.extract(input_file_path)
            # 抽出失敗した場合はスキップ
            if extract_result is None:
                # print(f"extract fault. path: {input_file_path}, method: {extractor.method}", file=sys.stdout)
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
        session.commit()
        # セッションをクローズ
        session.close()
    except TimeoutError as e:
        print(f"path: {input_file_path}", file=sys.stderr)
        print(e, file=sys.stderr)

    except Exception as e:
        # print(f"{str(e)} path: {input_file_path}")
        print(f"path: {input_file_path}", file=sys.stderr)
        session.rollback()
        session.close()
        raise e
