
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
import uuid
from database_engine import Base, engine

# Fileモデルクラスを定義
class Document(Base):
    __tablename__ = 'document'

    document_id = Column(String, primary_key=True)
    hash = Column(String)
    size = Column(Integer)

    # ファイルとページのリレーションシップを設定
    pages = relationship("Page", back_populates="document")
    # file_paths = relationship("FilePath", back_populates="document")

    def __str__(self):
        return "aaaa"


class PdfDocument(Document):
    __tablename__ = 'pdf_document'

    document_id = Column(String, ForeignKey("document.document_id"), primary_key=True)

    def __str__(self):
        return "aaaa"

class ImageDocument(Document):
    __tablename__ = 'image_document'

    document_id = Column(String, ForeignKey("document.document_id"), primary_key=True)

    def __str__(self):
        return "aaaa"

class PlainTextDocument(Document):
    __tablename__ = 'plain_text_document'

    document_id = Column(String, ForeignKey("document.document_id"), primary_key=True)

    def __str__(self):
        return "aaaa"

# データベースへのレコード追加関数
def insert_document(hash: str, size: int) -> str:
    # データベースセッションを作成
    Session = sessionmaker(bind=engine)
    session = Session()

    uuid_value = str(uuid.uuid4())
    document = Document(document_id=uuid_value, hash=hash, size=size, pages=[])
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

