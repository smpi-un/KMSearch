from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
import uuid
from database_engine import Base, engine

# Ocrモデルクラスを定義
class OcrText(Base):
    __tablename__ = 'ocr_text'

    ocr_text_id = Column(String, primary_key=True)
    ocr_id = Column(String, ForeignKey("ocr.ocr_id"))
    box_0_x = Column(Integer)
    box_0_y = Column(Integer)
    box_1_x = Column(Integer)
    box_1_y = Column(Integer)
    box_2_x = Column(Integer)
    box_2_y = Column(Integer)
    box_3_x = Column(Integer)
    box_3_y = Column(Integer)
    text = Column(String)
    confident = Column(Float)

    ocr = relationship("Ocr", back_populates="ocr_texts")


    def __str__(self):
        return "aaaa"


# データベースへのレコード追加関数
def insert_ocr_text(ocr_id: str, ocr_dict: dict) -> str:
    # データベースセッションを作成
    Session = sessionmaker(bind=engine)
    session = Session()

    uuid_value = str(uuid.uuid4())
    ocr_data = OcrText(ocr_text_id=uuid_value, ocr_id=ocr_id,
                       box_0_x=ocr_dict["boxes"][0][0], box_0_y=ocr_dict["boxes"][0][1],
                       box_1_x=ocr_dict["boxes"][1][0], box_1_y=ocr_dict["boxes"][1][1],
                       box_2_x=ocr_dict["boxes"][2][0], box_2_y=ocr_dict["boxes"][2][1],
                       box_3_x=ocr_dict["boxes"][3][0], box_3_y=ocr_dict["boxes"][3][1],
                       text=ocr_dict["text"],
                       confident=ocr_dict["confident"],
    )
    session.add(ocr_data)
    session.commit()

    # セッションをクローズ
    session.close()
    return uuid_value

# データベースからデータを取得する関数
def fetch_ocr_text() -> OcrText:
    Session = sessionmaker(bind=engine)
    session = Session()
    ocr_text = session.query(OcrText).all()
    session.close()
    return ocr_text

