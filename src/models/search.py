from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, JSON
from sqlalchemy.orm import sessionmaker, relationship
import uuid
from database_engine import Base, engine
from datetime import datetime

# Pageモデルクラスを定義
class SearchText(Base):
    __tablename__ = 'search_text'

    search_text_id = Column(String, primary_key=True)
    extract_id = Column(String, ForeignKey("extract.extract_id"))
    text = Column(String)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ページからファイルへのリレーションシップを設定
    extract = relationship("Extract", back_populates="search_texts")

    def __repr__(self):
        return f"<SearchText(search_text_id={self.search_text_id}, extract_id={self.extract_id}, text={self.text}, details={self.details}, created_at={self.created_at}, updated_at={self.updated_at})>"


    def to_dict(self):
        return {
             "searchTextId": self.search_text_id,
             "extractId": self.extract_id,
             "text": self.text,
             "details": self.details,
         }
Base.metadata.create_all(engine)

# データベースへのレコード追加関数
def insert_search_text(extract_id: str, text: int, details: str) -> str:
    # データベースセッションを作成
    Session = sessionmaker(bind=engine)
    session = Session()

    uuid_value = str(uuid.uuid4())
    new_search_text = SearchText(
        search_text_id=uuid_value, 
        extract_id=extract_id, 
        text=text,
        details=details,
        )
    session.add(new_search_text)
    session.commit()

    # セッションをクローズ
    session.close()
    return uuid_value

# データベースからデータを取得する関数
def fetch_page_data() -> SearchText:
    Session = sessionmaker(bind=engine)
    session = Session()
    page_data = session.query(SearchText).all()
    session.close()
    return page_data



