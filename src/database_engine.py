from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import json
from datetime import datetime
from utils.jsonencoder import DateTimeEncoder

database_name = 'kmsearch.sqlite'
# データベースのURLを指定してエンジンを作成
db_url = f"sqlite:///{database_name}"
# engine = create_engine(db_url)
engine = create_engine(
    db_url,
    json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False, indent=2, cls=DateTimeEncoder))

# ベースモデルを作成
Base = declarative_base()

import models
def create_all_database():
    # データベースとテーブルを作成
    Base.metadata.create_all(engine)
    # print(dir(models.Document))

create_all_database()
