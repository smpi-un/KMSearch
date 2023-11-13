from sqlalchemy import Column, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
import uuid
from database_engine import Base, engine
from datetime import datetime

# extractモデルクラスを定義
class Extract(Base):
    __tablename__ = 'extract'

    extract_id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey("document.document_id"))
    result = Column(JSON)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    document = relationship("Document", back_populates="extracts")
    search_texts = relationship("SearchText", back_populates="extract")

    def to_dict(self):
        return {
            "extract_id": self.extract_id,
            "document_id": self.document_id,
            # "extract_result_json": self.extract_result_json,
        }

    def __repr__(self):
        return f"<Extract(extract_id={self.extract_id}, document_id={self.document_id}, model_language={self.model_language}, custom_model_path={self.custom_model_path}, created_at={self.created_at}, updated_at={self.updated_at})>"


# データベースへのレコード追加関数
def insert_extract_data(document_id: str, result: any, details: any) -> str:
    # データベースセッションを作成
    Session = sessionmaker(bind=engine)
    session = Session()

    uuid_value = str(uuid.uuid4())
    extract_data = Extract(extract_id=uuid_value, document_id=document_id, result=result, details=details)
    session.add(extract_data)
    session.commit()

    # セッションをクローズ
    session.close()
    return uuid_value

# データベースからデータを取得する関数
def fetch_extract_data() -> Extract:
    Session = sessionmaker(bind=engine)
    session = Session()
    extract_data = session.query(Extract).all()
    session.close()
    return extract_data
