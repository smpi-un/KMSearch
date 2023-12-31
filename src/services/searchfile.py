from sqlalchemy.orm import joinedload
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from database_engine import get_engine
import json
from models import *
from lark import Tree
import utils.formulaparser
import sys
from typing import Literal

def tree_to_cond(tree: Tree):
    match tree.data:
        case "and_expr":
            expr1 = tree_to_cond(tree.children[0])
            expr2 = tree_to_cond(tree.children[1])
            return and_(expr1, expr2)
        case "or_expr":
            expr1 = tree_to_cond(tree.children[0])
            expr2 = tree_to_cond(tree.children[1])
            return or_(expr1, expr2)
        case "word":
            return SearchText.text.contains(tree.children[0].value)
        case "not_expr":
            return ~tree_to_cond(tree.children[0])
        case _:
            raise tree.data

def search(keyword: str, unit: Literal["word", "page", "file"], extract_method: str, file_path_pattern: str, out_path: str):
  
    Session = sessionmaker(bind=get_engine())
    session = Session()
  
    # OcrTextとOcrを結合してデータを取得し、さらにPageを結合
    query1 = (
        session.query(Document, File, Extract, SearchText, )
        .join(File, Document.document_id == File.document_id)
        .join(Extract, Document.document_id == Extract.document_id)
        .join(SearchText, Extract.extract_id == SearchText.extract_id)
    )
    unit = "page"
    query2 = query1.filter(tree_to_cond(utils.formulaparser.parse_formula(keyword))) if keyword is not None else query1
    query3 = query2.filter(Extract.method == extract_method) if extract_method is not None else query2
    query4 = query3.filter(File.path.like(f"%{file_path_pattern}%")) if file_path_pattern is not None else query3
    query5 = query4.filter(SearchText.unit == unit) if unit is not None else query4
    result = query5.all()

    # データを整理して階層構造のJSON形式に変換
    document_dict = {}
    for document, file, extract, search_text  in result:
  
      if document.document_id not in document_dict:
          document_dict[document.document_id] = document.to_dict()
          document_dict[document.document_id]["extract"] = dict()
          document_dict[document.document_id]["file"] = dict()
      extract_dict = document_dict[document.document_id]["extract"]
      file_dict = document_dict[document.document_id]["file"]
  
      if file.file_id not in file_dict:
          file_dict[file.file_id] = file.to_dict()
  
      if extract.extract_id not in extract_dict:
          extract_dict[extract.extract_id] = extract.to_dict()
          extract_dict[extract.extract_id]["searchText"] = dict()
      search_text_dict = extract_dict[extract.extract_id]["searchText"]
  
      if search_text.search_text_id not in search_text_dict:
          search_text_dict[search_text.search_text_id] = search_text.to_dict()
  
    # JSON形式に変換して出力
    json_data = json.dumps({"status": "success", "data": document_dict}, indent=2, ensure_ascii=False)
    
    # 結果を、出力先ファイルパスがある場合はファイルへ、ない場合は標準出力へ出力。
    if out_path is None or out_path == '':
        print(json_data, file=sys.stdout)
    else:
        with open(out_path, 'w', encoding='utf-8') as fp:
            fp.write(json_data)