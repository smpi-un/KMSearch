
from sqlalchemy.orm import sessionmaker
from database_engine import engine
import json
from models import *
import utils.filehash as filehash
import sys

def show_document(path:str, out_path: str) -> int:
    hash = filehash.calculate_file_hash(path)
    if hash is None:
        print(f"hash is None. path = {path}", file=sys.stderr)
        return 1

    Session = sessionmaker(bind=engine)
    session = Session()

    # OcrTextとOcrを結合してデータを取得し、さらにPageを結合
    result = (
        session.query(Document)
        .join(File, Document.document_id == File.document_id)
        .filter(Document.hash == hash)  # ハッシュが一致するもののみ
        .all()
    )

    # データを整理して階層構造のJSON形式に変換
    document_dict = dict()
    for document  in result:
      if document.document_id not in document_dict:
          document_dict[document.document_id] = document.to_dict()
          extract_dict = dict()
          for extract in document.extracts:
              extract_dict[extract.extract_id] = extract.to_dict()
              search_text_dict = dict()
              for search_text in extract.search_texts:
                  search_text_dict[search_text.search_text_id] = search_text.to_dict()
              extract_dict[extract.extract_id]["searchTexts"] = search_text_dict
          file_dict = dict()
          for file in document.files:
              file_dict[file.file_id] = file.to_dict()
          document_dict[document.document_id]["extract"] = extract_dict
          document_dict[document.document_id]["file"] = file_dict

    # JSON形式に変換して出力
    json_data = json.dumps(document_dict, indent=2, ensure_ascii=False)

    # 結果を、出力先ファイルパスがある場合はファイルへ、ない場合は標準出力へ出力。
    if out_path is None or out_path == '':
        print(json_data, file=sys.stdout)
    else:
        with open(out_path, 'w', encoding='utf-8') as fp:
            print(json_data, file=fp)