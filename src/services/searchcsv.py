import pandas as pd
from sqlalchemy.orm import joinedload
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from database_engine import engine
import json
from models import *
import re

def search(expression: str):

  Session = sessionmaker(bind=engine)
  session = Session()

  # OcrTextとOcrを結合してデータを取得し、さらにPageを結合
  query = (
      session.query(Document, File, Extract, SearchText, )
      .join(File, Document.document_id == File.document_id)
      .join(Extract, Document.document_id == Extract.document_id)
      .join(SearchText, Extract.extract_id == SearchText.extract_id)
      # .options(joinedload(Document.extracts), joinedload(Extract.).joinedload(Extract.extract_texts))
      # .filter(SearchText.text.like(f"%{keyword}%"))  # キーワードが含まれるもののみ取得
      # .filter(OcrText.confident >= 0.4)  # confidentが0.4以上のもののみ取得
      # .filter(func.length(SearchText.text) >= 2)  # textの長さが2以上のもののみ取得
      # .all()
  )
  print(str(query))
  df = pd.read_sql_query(str(query), con=engine)
  print(df)
  print(query_df(df,expression))
  session.close()

def query_df(df, query_str):
    search_list = []
    pattern = re.compile(r'(\w+)\s*contains\s*"(.*)"')
    m = pattern.findall(query_str)

    if m:
        for column, value in m:
            mask = df[column].str.contains(value, regex=False)
            df = df[mask]
            search_list.append(column + ' contains "' + value +'"')

    for item in search_list:
        query_str = query_str.replace(item, '')

    query_str = ' '.join(query_str.split())

    if query_str:  # checking whether query_str is empty 
        print(f"final query_str is: {query_str}")  # print query_str to debug 
        df = df.query(query_str, engine=engine)

    return df
