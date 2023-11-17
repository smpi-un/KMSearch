from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship, Session
import uuid
from database_engine import Base, engine
from datetime import datetime

# Fileモデルクラスを定義
class File(Base):
    __tablename__ = 'file'

    file_id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey("document.document_id"))
    path = Column(String)
    missing = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    document = relationship("Document", back_populates="files")

    def to_dict(self):
        return {
             "fileId": self.file_id,
             "documentId": self.document_id,
             "path": self.path,
             "missing": self.missing,
         }

# データベースへのレコード追加関数
def insert_file(session: Session, document_id: str, path: str, missing: bool) -> str:

    uuid_value = str(uuid.uuid4())
    file_data = File(file_id=uuid_value, document_id=document_id, path=path, missing=missing)
    session.add(file_data)

    return uuid_value

# データベースからデータを取得する関数
def fetch_file() -> File:
    Session = sessionmaker(bind=engine)
    session = Session()
    file = session.query(File).all()
    session.close()
    return file


def get_file_id_by_hash(session: Session, path: str) -> str:
    """ 
    ファイルパスを引数にとり、保存済みのFileテーブルから同じhashが存在する場合そのfile_idを返す関数.

    Parameters:
    hash_value (str): チェックするhash value 

    Returns:
    str: ファイルパスが存在する場合、そのfile_id. 存在しなければ None
    """

    file = session.query(File).filter(File.path == path).first()
    return file.file_id if file else None

def update_document_id(session: Session, file_id, new_document_id):

    # 指定したfile_idのレコードを見つける
    file = session.query(File).get(file_id)

    # document_idを新しいものに更新する
    file.document_id = new_document_id
    