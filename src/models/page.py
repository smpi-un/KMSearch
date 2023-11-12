from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
import uuid
from database_engine import Base, engine
from datetime import datetime

# Pageモデルクラスを定義
class Page(Base):
    __tablename__ = 'page'

    page_id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey("document.document_id"))
    page_number = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ocrs = relationship("Ocr", back_populates="page")
    # ページからファイルへのリレーションシップを設定
    document = relationship("Document", back_populates="pages")

    def __repr__(self):
        return f"<Page(page_id={self.page_id}, document_id={self.document_id}, page_number={self.page_number}, created_at={self.created_at}, updated_at={self.updated_at})>"


    def to_dict(self):
        return {
             "page_id": self.page_id,
             "document_id": self.document_id,
             "page_number": self.page_number
         }
Base.metadata.create_all(engine)

# データベースへのレコード追加関数
def insert_page_data(document_id: str, page_number: int) -> str:
    # データベースセッションを作成
    Session = sessionmaker(bind=engine)
    session = Session()

    uuid_value = str(uuid.uuid4())
    page_data = Page(page_id=uuid_value, document_id=document_id, page_number=page_number)
    session.add(page_data)
    session.commit()

    # セッションをクローズ
    session.close()
    return uuid_value

# データベースからデータを取得する関数
def fetch_page_data() -> Page:
    Session = sessionmaker(bind=engine)
    session = Session()
    page_data = session.query(Page).all()
    session.close()
    return page_data


