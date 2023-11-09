from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker
import uuid
from database_engine import Base, engine

# Fileモデルクラスを定義
class FilePath(Base):
    __tablename__ = 'file_path'

    file_path_id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey("document.document_id"))
    file_path = Column(String)
    missing = Column(Boolean)

    def __str__(self):
        return "aaaa"

# データベースへのレコード追加関数
def insert_file_path(document_id: str, file_path: str, missing: bool) -> str:
    # データベースセッションを作成
    Session = sessionmaker(bind=engine)
    session = Session()

    uuid_value = str(uuid.uuid4())
    file_path_data = FilePath(file_path_id=uuid_value, document_id=document_id, file_path=file_path, missing=missing)
    session.add(file_path_data)
    session.commit()

    # セッションをクローズ
    session.close()

    return uuid_value

# データベースからデータを取得する関数
def fetch_file_path() -> FilePath:
    Session = sessionmaker(bind=engine)
    session = Session()
    file_path = session.query(FilePath).all()
    session.close()
    return file_path

