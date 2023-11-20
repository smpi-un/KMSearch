from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import json
from datetime import datetime
from utils.jsonencoder import DateTimeEncoder

engine = None

def get_engine():
    global engine
    return engine

def init_engine(db_url):
    """DBのURLからengineを初期化する関数"""
    global engine
    engine = create_engine(db_url)
    init_database()



# ベースモデルを作成
Base = declarative_base()

def init_database():
    import models
    def create_all_database():
        # データベースとテーブルを作成
        Base.metadata.create_all(engine)
        # print(dir(models.Document))

    create_all_database()



# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# import json
# from datetime import datetime
# from utils.jsonencoder import DateTimeEncoder
# 
# def init_database(db_url: str):
#     print(db_url)
#     # global engine
#     # database_name = 'kmsearch.sqlite'
#     # # データベースのURLを指定してエンジンを作成
#     # db_url = f"sqlite:///{database_name}"
#     # # engine = create_engine(db_url)
#     engine = create_engine(
#         db_url,
#         json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False, indent=2, cls=DateTimeEncoder))
#     create_all_database(engine)
#     return engine
# 
# # ベースモデルを作成
# Base = declarative_base()
# 
# # db作成前に全モデルを読み込む
# def create_all_database(engine):
#     import models
#     # データベースとテーブルを作成
#     Base.metadata.create_all(engine)
#     # print(dir(models.Document))
# 
# 