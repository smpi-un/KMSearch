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
      session.query(OcrText, Ocr, Page, Document)
      .join(Ocr, OcrText.ocr_id == Ocr.ocr_id)
      .join(Page, Ocr.page_id == Page.page_id)
      .join(Document, Page.document_id == Document.document_id)
      .options(joinedload(OcrText.ocr), joinedload(OcrText.ocr).joinedload(Ocr.ocr_texts))
      .filter(OcrText.text.like(f"%{keyword}%"))  # キーワードが含まれるもののみ取得
      .filter(OcrText.confident >= 0.4)  # confidentが0.4以上のもののみ取得
      .filter(func.length(OcrText.text) >= 2)  # textの長さが2以上のもののみ取得
      .all()
  )

  # データを整理して階層構造のJSON形式に変換
  file_dict = {}
  print(len(result))
  for ocr_text, ocr, page, document in result:
    if file.file_id not in file_dict:
        file_dict[file.file_id] = file.to_dict()
        file_dict[file.file_id]["document"] = dict()
    document_dict = file_dict[file.file_id]["document"]

    if document.document_id not in document_dict:
        document_dict[document.document_id] = document.to_dict()
        document_dict[document.document_id]["page"] = dict()
    page_dict = document_dict[document.document_id]["page"]

    if page.page_id not in page_dict:
        page_dict[page.page_id] = page.to_dict()
        page_dict[page.page_id]["ocr"] = dict()
    ocr_dict = page_dict[page.page_id]["ocr"]

    if ocr.ocr_id not in ocr_dict:
        ocr_dict[ocr.ocr_id] = ocr.to_dict()
        ocr_dict[ocr.ocr_id]["ocr_text"] = dict()
    ocr_text_dict = ocr_dict[ocr.ocr_id]["ocr_text"]

    if ocr_text.ocr_text_id not in ocr_text_dict:
        ocr_text_dict[ocr_text.ocr_text_id] = ocr_text.to_dict()

    
    # if page.page_id not in data:
    #     data[page.page_id] = {
    #         "page_id": page.page_id,
    #         "document_id": page.document_id,
    #         "page_number": page.page_number
    #     }




  # JSON形式に変換して出力
  json_data = json.dumps(file_dict, indent=2, ensure_ascii=False)

  print(json_data)