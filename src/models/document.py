
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship, Session
import uuid
from database_engine import Base, engine
from datetime import datetime


# Fileモデルクラスを定義
class Document(Base):
    __tablename__ = 'document'

    document_id = Column(String, primary_key=True)
    hash = Column(String)
    size = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    files = relationship("File", back_populates="document")
    extracts = relationship("Extract", back_populates="document")

    def to_dict(self):
        return {
             "document_id": self.document_id,
             "hash": self.hash,
             "size": self.size
         }

    def __str__(self):
        return "aaaa"


# データベースへのレコード追加関数
def insert_document(hash: str, size: int) -> str:
    # データベースセッションを作成
    Session = sessionmaker(bind=engine)
    session = Session()

    uuid_value = str(uuid.uuid4())
    document = Document(document_id=uuid_value, hash=hash, size=size)
    session.add(document)
    session.commit()

    # セッションをクローズ
    session.close()

    return uuid_value

# データベースからデータを取得する関数
def fetch_document() -> Document:
    Session = sessionmaker(bind=engine)
    session = Session()
    document = session.query(Document).all()
    session.close()
    return document


def get_document_id_by_hash(hash_value: str) -> str:
    """ 
    ハッシュ値を引数にとり、保存済みのDocumentテーブルから同じhashが存在する場合そのdocument_idを返す関数.

    Parameters:
    db (Session): SQLAlchemy session
    hash_value (str): チェックするhash value 

    Returns:
    str: ハッシュ値が存在する場合、そのdocument_id. 存在しなければ None
    """

    Session = sessionmaker(bind=engine)
    session = Session()
    document = session.query(Document).filter(Document.hash == hash_value).first()
    # セッションをクローズ
    session.close()
    return document.document_id if document else None
