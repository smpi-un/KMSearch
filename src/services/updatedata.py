import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_engine import engine
from models import *




def update(model_path):
  update_files()
def update_files():
  Session = sessionmaker(bind=engine)
  session = Session()

  # 全てのFileデータを取得
  files = session.query(File).all()

  # 各ファイルが実際に存在するかを確認
  for file in files:
      # ファイルが存在するか確認
      if os.path.exists(file.path):
          if file.missing is not False:
              print(f'missing: {file.path}')
              # ファイルが存在し、file.missingがFalseでない場合、file.missingをFalseに更新
              file.missing = False
              session.add(file)  # 更新をスケジュール
      else:
          if file.missing is not True:
              print(f'found: {file.path}')
              # ファイルが存在せず、file.missingがTrueでない場合、file.missingをTrueに更新
              file.missing = True
              session.add(file)  # 更新をスケジュール

  # データベースへの更新をコミット
  session.commit()
