from sqlalchemy import Column, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
import uuid
from database_engine import Base, engine
from datetime import datetime

# Ocrモデルクラスを定義
class Ocr(Base):
    __tablename__ = 'ocr'

    ocr_id = Column(String, primary_key=True)
    page_id = Column(String, ForeignKey("page.page_id"))
    model_language = Column(String)
    custom_model_path = Column(String)
    ocr_result_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ocr_texts = relationship("OcrText", back_populates="ocr")
    page = relationship("Page", back_populates="ocrs")

    def to_dict(self):
        return {
            "ocr_id": self.ocr_id,
            "page_id": self.page_id,
            "model_language": self.model_language,
            "custom_model_path": self.custom_model_path,
            # "ocr_result_json": self.ocr_result_json,
        }
    def to_all_dict(self):
        return {
            "ocr_id": self.ocr_id,
            "page_id": self.page_id,
            "model_language": self.model_language,
            "custom_model_path": self.custom_model_path,
            # "ocr_result_json": self.ocr_result_json,
            "ocr_texts": [ocr_text.to_dict() for ocr_text in self.ocr_texts],
        }

    def __repr__(self):
        return f"<Ocr(ocr_id={self.ocr_id}, page_id={self.page_id}, model_language={self.model_language}, custom_model_path={self.custom_model_path}, created_at={self.created_at}, updated_at={self.updated_at})>"


# データベースへのレコード追加関数
def insert_ocr_data(page_id: str, model_language: str, custom_model_path: str, ocr_result_json: str) -> str:
    # データベースセッションを作成
    Session = sessionmaker(bind=engine)
    session = Session()

    uuid_value = str(uuid.uuid4())
    ocr_data = Ocr(ocr_id=uuid_value, page_id=page_id, model_language=model_language, custom_model_path=custom_model_path, ocr_result_json=ocr_result_json)
    session.add(ocr_data)
    session.commit()

    # セッションをクローズ
    session.close()
    return uuid_value

# データベースからデータを取得する関数
def fetch_ocr_data() -> Ocr:
    Session = sessionmaker(bind=engine)
    session = Session()
    ocr_data = session.query(Ocr).all()
    session.close()
    return ocr_data
