from sqlalchemy.orm import joinedload
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from database_engine import engine
import json
from models import *

def search(keyword):

  Session = sessionmaker(bind=engine)
  session = Session()

  # OcrTextとOcrを結合してデータを取得し、さらにPageを結合
  result = (
      session.query(Document, File, Extract, SearchText, )
      .join(File, Document.document_id == File.document_id)
      .join(Extract, Document.document_id == Extract.document_id)
      .join(SearchText, Extract.extract_id == SearchText.extract_id)
      # .options(joinedload(Document.extracts), joinedload(Extract.).joinedload(Extract.extract_texts))
      .filter(SearchText.text.like(f"%{keyword}%"))  # キーワードが含まれるもののみ取得
      # .filter(OcrText.confident >= 0.4)  # confidentが0.4以上のもののみ取得
      .filter(func.length(SearchText.text) >= 2)  # textの長さが2以上のもののみ取得
      .all()
  )

  # データを整理して階層構造のJSON形式に変換
  file_dict = {}
  print(len(result))
  for document, file, extract, search_text  in result:
    if file.file_id not in file_dict:
        file_dict[file.file_id] = file.to_dict()
        file_dict[file.file_id]["document"] = dict()
    document_dict = file_dict[file.file_id]["document"]

    if document.document_id not in document_dict:
        document_dict[document.document_id] = document.to_dict()
        document_dict[document.document_id]["page"] = dict()
    page_dict = document_dict[document.document_id]["page"]

    if extract.page_id not in page_dict:
        page_dict[extract.page_id] = extract.to_dict()
        page_dict[extract.page_id]["ocr"] = dict()
    ocr_dict = page_dict[extract.page_id]["ocr"]

    if file.ocr_id not in ocr_dict:
        ocr_dict[file.ocr_id] = file.to_dict()
        ocr_dict[file.ocr_id]["ocr_text"] = dict()
    ocr_text_dict = ocr_dict[file.ocr_id]["ocr_text"]

    if search_text.ocr_text_id not in ocr_text_dict:
        ocr_text_dict[search_text.ocr_text_id] = search_text.to_dict()

    
    # if page.page_id not in data:
    #     data[page.page_id] = {
    #         "page_id": page.page_id,
    #         "document_id": page.document_id,
    #         "page_number": page.page_number
    #     }




  # JSON形式に変換して出力
  json_data = json.dumps(file_dict, indent=2, ensure_ascii=False)

  print(json_data)